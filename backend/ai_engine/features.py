"""
Feature Extraction for AI Signal Intelligence & Modulation Classification.
Extracts 18 robust statistical, spectral, temporal, and constellation features
from raw complex baseband I/Q sample bursts.
"""

from typing import Dict, List, Tuple
import numpy as np
from scipy.signal import welch

FEATURE_NAMES = [
    "C20_abs",
    "C40_abs",
    "C41_abs",
    "C42_abs",
    "C63_abs",
    "gamma_max",
    "sigma_ap",
    "sigma_af",
    "papr_db",
    "spectral_flatness",
    "spectral_kurtosis",
    "spectral_rolloff",
    "spectral_centroid",
    "radial_moment_r42",
    "constellation_entropy",
    "envelope_skewness",
    "envelope_kurtosis",
    "zero_crossing_rate",
]


def extract_signal_features(
    samples: np.ndarray,
    sample_rate: float = 1e6,
    max_samples: int = 65536,
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Extract a 18-dimensional normalized feature vector from complex I/Q samples.
    Returns:
        (feature_vector: np.ndarray, feature_dict: Dict[str, float])
    """
    if len(samples) < 128:
        # Fallback for empty/short signal
        zeros = np.zeros(len(FEATURE_NAMES), dtype=np.float32)
        return zeros, {name: 0.0 for name in FEATURE_NAMES}

    # Slice and normalize to unit average power
    sig = samples[:max_samples].astype(np.complex64)
    sig = sig - np.mean(sig)
    pwr = np.mean(np.abs(sig) ** 2)
    if pwr < 1e-14:
        zeros = np.zeros(len(FEATURE_NAMES), dtype=np.float32)
        return zeros, {name: 0.0 for name in FEATURE_NAMES}

    x = sig / np.sqrt(pwr)
    N = len(x)

    # 1. Higher-Order Cumulants
    m20 = np.mean(x ** 2)
    m21 = np.mean(np.abs(x) ** 2)
    m40 = np.mean(x ** 4)
    m41 = np.mean(x ** 3 * np.conj(x))
    m42 = np.mean(np.abs(x) ** 4)
    m63 = np.mean(np.abs(x) ** 6)

    c20 = m20
    c40 = m40 - 3.0 * (m20 ** 2)
    c41 = m41 - 3.0 * m20 * m21
    c42 = m42 - (np.abs(m20) ** 2) - 2.0 * (m21 ** 2)
    c63 = m63 - 9.0 * c42 * m21 - 6.0 * (m21 ** 3)

    c20_abs = float(np.abs(c20))
    c40_abs = float(np.abs(c40))
    c41_abs = float(np.abs(c41))
    c42_abs = float(np.abs(c42))
    c63_abs = float(np.abs(c63))

    # 2. Instantaneous Amplitude, Phase, Frequency
    amp = np.abs(x)
    amp_norm = (amp / (np.mean(amp) + 1e-12)) - 1.0

    # Gamma max: max of normalized PSD of centered instantaneous amplitude
    fft_amp = np.abs(np.fft.fft(amp_norm)) ** 2 / N
    gamma_max = float(np.max(fft_amp) if len(fft_amp) > 0 else 0.0)

    # Instantaneous phase & frequency
    # Filter out near-zero amplitude points for stable phase calculation
    thresh = 0.1 * np.mean(amp)
    valid_mask = amp > thresh
    if np.sum(valid_mask) > 100:
        valid_x = x[valid_mask]
        phase = np.unwrap(np.angle(valid_x))
        # Remove linear trend (carrier offset)
        t_idx = np.arange(len(phase))
        p = np.polyfit(t_idx, phase, 1)
        detrended_phase = phase - (p[0] * t_idx + p[1])
        sigma_ap = float(np.std(detrended_phase))

        # Instantaneous frequency
        diff_phase = np.diff(phase)
        sigma_af = float(np.std(diff_phase) / (2.0 * np.pi))
    else:
        sigma_ap = 1.0
        sigma_af = 0.5

    # PAPR (Peak to Average Power Ratio) in dB
    peak_pwr = np.max(np.abs(x) ** 2)
    avg_pwr = np.mean(np.abs(x) ** 2) + 1e-12
    papr_db = float(10.0 * np.log10(peak_pwr / avg_pwr))

    # 3. Spectral Features via Welch PSD
    nperseg = min(1024, max(128, N // 8))
    freqs, psd = welch(x, fs=sample_rate, nperseg=nperseg, return_onesided=False)
    psd = np.fft.fftshift(psd)
    freqs = np.fft.fftshift(freqs)
    psd_norm = psd / (np.sum(psd) + 1e-12)

    # Spectral Flatness Measure (geometric mean / arithmetic mean)
    log_psd = np.log(psd_norm + 1e-12)
    geom_mean = np.exp(np.mean(log_psd))
    arith_mean = np.mean(psd_norm)
    spectral_flatness = float(geom_mean / (arith_mean + 1e-12))

    # Spectral Kurtosis of PSD
    psd_mean = np.mean(psd)
    psd_std = np.std(psd) + 1e-12
    spectral_kurtosis = float(np.mean(((psd - psd_mean) / psd_std) ** 4))

    # Spectral Centroid
    spectral_centroid = float(np.sum(freqs * psd_norm) / (np.sum(psd_norm) + 1e-12) / (sample_rate / 2.0))

    # Spectral Rolloff (95% power threshold)
    cumsum_psd = np.cumsum(psd_norm)
    rolloff_idx = np.searchsorted(cumsum_psd, 0.95)
    rolloff_freq = np.abs(freqs[min(rolloff_idx, len(freqs) - 1)])
    spectral_rolloff = float(rolloff_freq / (sample_rate / 2.0))

    # 4. Constellation Geometry & Moments
    r42 = float(m42 / (m21 ** 2 + 1e-12))

    # Constellation 2D Entropy (16x16 grid)
    i_bins = np.linspace(-2.5, 2.5, 17)
    q_bins = np.linspace(-2.5, 2.5, 17)
    h2d, _, _ = np.histogram2d(x.real, x.imag, bins=[i_bins, q_bins])
    h2d_prob = h2d.flatten() / (N + 1e-12)
    h2d_prob = h2d_prob[h2d_prob > 0]
    constellation_entropy = float(-np.sum(h2d_prob * np.log2(h2d_prob)) / np.log2(256.0))

    # Envelope Skewness & Kurtosis
    amp_centered = amp - np.mean(amp)
    amp_std = np.std(amp) + 1e-12
    envelope_skewness = float(np.mean((amp_centered / amp_std) ** 3))
    envelope_kurtosis = float(np.mean((amp_centered / amp_std) ** 4))

    # Zero Crossing Rate of real part
    signs = np.sign(x.real)
    signs[signs == 0] = 1
    zero_crossing_rate = float(np.mean(np.abs(np.diff(signs)) > 0))

    feature_dict = {
        "C20_abs": c20_abs,
        "C40_abs": c40_abs,
        "C41_abs": c41_abs,
        "C42_abs": c42_abs,
        "C63_abs": c63_abs,
        "gamma_max": gamma_max,
        "sigma_ap": sigma_ap,
        "sigma_af": sigma_af,
        "papr_db": papr_db,
        "spectral_flatness": spectral_flatness,
        "spectral_kurtosis": spectral_kurtosis,
        "spectral_rolloff": spectral_rolloff,
        "spectral_centroid": spectral_centroid,
        "radial_moment_r42": r42,
        "constellation_entropy": constellation_entropy,
        "envelope_skewness": envelope_skewness,
        "envelope_kurtosis": envelope_kurtosis,
        "zero_crossing_rate": zero_crossing_rate,
    }

    feature_vector = np.array([feature_dict[k] for k in FEATURE_NAMES], dtype=np.float32)
    # Clip extreme outliers
    feature_vector = np.nan_to_num(feature_vector, nan=0.0, posinf=100.0, neginf=-100.0)

    return feature_vector, feature_dict
