"""
Instantaneous Signal Features — Amplitude, Phase, Frequency, and
Spectral Kurtosis extraction for signal characterization.
"""

import numpy as np
from scipy.signal import hilbert


def instantaneous_amplitude(samples: np.ndarray) -> np.ndarray:
    """Compute instantaneous amplitude (envelope) of a complex signal."""
    return np.abs(samples)


def instantaneous_phase(samples: np.ndarray, unwrap: bool = True) -> np.ndarray:
    """Compute instantaneous phase of a complex signal."""
    phase = np.angle(samples)
    if unwrap:
        phase = np.unwrap(phase)
    return phase


def instantaneous_frequency(
    samples: np.ndarray,
    sample_rate: float,
) -> np.ndarray:
    """
    Compute instantaneous frequency from the derivative of unwrapped phase.
    Returns array of length len(samples)-1 in Hz.
    """
    phase = instantaneous_phase(samples, unwrap=True)
    freq = np.diff(phase) / (2 * np.pi) * sample_rate
    return freq


def spectral_kurtosis(
    samples: np.ndarray,
    nfft: int = 256,
    noverlap: int = 128,
) -> dict:
    """
    Compute frequency-domain spectral kurtosis as a measure of
    non-Gaussianity at each frequency bin. Useful for detecting
    digitally modulated signals vs. noise.

    Returns dict:
        freqs   : normalized frequency bins (0..1)
        sk      : spectral kurtosis values per frequency bin
    """
    step = nfft - noverlap
    n_frames = max(1, (len(samples) - nfft) // step + 1)

    # Accumulate power spectra
    S2 = np.zeros(nfft)
    S4 = np.zeros(nfft)

    for i in range(n_frames):
        seg = samples[i * step : i * step + nfft]
        if len(seg) < nfft:
            break
        X = np.fft.fft(seg, nfft)
        P = np.abs(X) ** 2
        S2 += P
        S4 += P ** 2

    S2 /= n_frames
    S4 /= n_frames

    # Spectral kurtosis: SK = (M * S4 / S2^2) - 1
    # For Gaussian noise, SK ≈ 0; for modulated signals, SK differs.
    sk = np.zeros(nfft)
    mask = S2 > 1e-30
    sk[mask] = (n_frames * S4[mask] / (S2[mask] ** 2 + 1e-30)) - 1

    freqs = np.linspace(0, 1, nfft)
    return {"freqs": freqs.tolist(), "sk": sk.tolist()}


def compute_all_features(
    samples: np.ndarray,
    sample_rate: float,
    max_points: int = 4096,
) -> dict:
    """Compute all instantaneous features for GUI display."""
    sig = samples[:max_points]
    t = np.arange(len(sig)) / sample_rate

    amp = instantaneous_amplitude(sig)
    phase = instantaneous_phase(sig)
    freq = instantaneous_frequency(sig, sample_rate)

    return {
        "times": t.tolist(),
        "amplitude": amp.tolist(),
        "phase": phase.tolist(),
        "inst_freq": freq.tolist(),
        "inst_freq_times": t[:-1].tolist(),
    }
