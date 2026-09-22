"""
Spectral Analysis — FFT, Welch PSD, STFT Spectrogram / Waterfall, and
Occupied Bandwidth (OBW) estimation.
"""

import numpy as np
from scipy.signal import welch, stft, get_window


def compute_fft(
    samples: np.ndarray,
    sample_rate: float,
    nfft: int = 1024,
    window: str = "hann",
) -> dict:
    """
    Compute single-sided (complex baseband) FFT magnitude spectrum.

    Returns dict with:
        freqs   : frequency axis (Hz), centered around 0
        mag_db  : magnitude in dB (relative to peak)
    """
    n = min(len(samples), nfft)
    win = get_window(window, n)
    windowed = samples[:n] * win
    X = np.fft.fftshift(np.fft.fft(windowed, nfft))
    mag = np.abs(X)
    mag_db = 20 * np.log10(mag / (np.max(mag) + 1e-30) + 1e-30)
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft, 1.0 / sample_rate))
    return {"freqs": freqs.tolist(), "mag_db": mag_db.tolist()}


def compute_psd(
    samples: np.ndarray,
    sample_rate: float,
    nfft: int = 1024,
    nperseg: int = 0,
    window: str = "hann",
) -> dict:
    """
    Compute Power Spectral Density using Welch's method.

    Returns dict with:
        freqs    : frequency axis (Hz)
        psd_db   : PSD in dB/Hz
    """
    if nperseg <= 0:
        nperseg = min(nfft, len(samples))

    f, Pxx = welch(
        samples,
        fs=sample_rate,
        window=window,
        nperseg=nperseg,
        nfft=nfft,
        return_onesided=False,
        scaling="density",
    )
    # Shift to center
    f = np.fft.fftshift(f)
    Pxx = np.fft.fftshift(Pxx)

    Pxx_db = 10 * np.log10(Pxx + 1e-30)

    return {"freqs": f.tolist(), "psd_db": Pxx_db.tolist()}


def compute_spectrogram(
    samples: np.ndarray,
    sample_rate: float,
    nfft: int = 512,
    window: str = "hann",
    noverlap: int = 0,
    max_time_bins: int = 512,
) -> dict:
    """
    Compute STFT-based spectrogram / waterfall.

    Returns dict with:
        times   : time axis (seconds) — list
        freqs   : frequency axis (Hz) — list
        mag_db  : 2D array [time_bins x freq_bins] in dB — list of lists
    """
    if noverlap <= 0:
        noverlap = nfft // 2

    # Limit length to avoid huge arrays
    max_samples = max_time_bins * (nfft - noverlap) + nfft
    sig = samples[:max_samples] if len(samples) > max_samples else samples

    f, t, Zxx = stft(
        sig,
        fs=sample_rate,
        window=window,
        nperseg=nfft,
        noverlap=noverlap,
        nfft=nfft,
        return_onesided=False,
    )

    # Shift frequencies to center
    f = np.fft.fftshift(f)
    Zxx = np.fft.fftshift(Zxx, axes=0)

    mag = np.abs(Zxx)
    mag_db = 20 * np.log10(mag + 1e-30)

    # Normalize to 0..1 for colormap
    vmin = np.percentile(mag_db, 5)
    vmax = np.max(mag_db)
    mag_norm = np.clip((mag_db - vmin) / (vmax - vmin + 1e-30), 0, 1)

    return {
        "times": t.tolist(),
        "freqs": f.tolist(),
        "mag_db": mag_db.T.tolist(),  # [time x freq] for row-major rendering
        "mag_norm": mag_norm.T.tolist(),
        "vmin": float(vmin),
        "vmax": float(vmax),
    }


def estimate_occupied_bandwidth(
    samples: np.ndarray,
    sample_rate: float,
    nfft: int = 4096,
    percent: float = 0.99,
) -> dict:
    """
    Estimate the occupied bandwidth (OBW) containing `percent`% of total
    integrated power.

    Returns dict with:
        obw_hz       : occupied bandwidth in Hz
        lower_freq   : lower edge frequency (Hz)
        upper_freq   : upper edge frequency (Hz)
        center_freq  : power centroid frequency (Hz)
    """
    f, Pxx = welch(
        samples, fs=sample_rate, nperseg=min(nfft, len(samples)),
        nfft=nfft, return_onesided=False, scaling="spectrum",
    )
    f = np.fft.fftshift(f)
    Pxx = np.fft.fftshift(Pxx)

    total_power = np.sum(Pxx)
    if total_power < 1e-30:
        return {"obw_hz": 0, "lower_freq": 0, "upper_freq": 0, "center_freq": 0}

    # CDF from lower freq up
    cumpower = np.cumsum(Pxx)
    threshold_lo = (1 - percent) / 2 * total_power
    threshold_hi = (1 + percent) / 2 * total_power

    idx_lo = np.searchsorted(cumpower, threshold_lo)
    idx_hi = np.searchsorted(cumpower, threshold_hi)
    idx_lo = max(0, min(idx_lo, len(f) - 1))
    idx_hi = max(0, min(idx_hi, len(f) - 1))

    lower = float(f[idx_lo])
    upper = float(f[idx_hi])
    obw = upper - lower

    # Power centroid
    center = float(np.sum(f * Pxx) / total_power)

    return {
        "obw_hz": obw,
        "lower_freq": lower,
        "upper_freq": upper,
        "center_freq": center,
    }


def compute_time_domain(
    samples: np.ndarray,
    sample_rate: float,
    max_points: int = 4096,
) -> dict:
    """
    Compute time-domain I/Q waveform for display.

    Returns dict with:
        times : time axis (seconds)
        i_values : real part
        q_values : imaginary part
        amplitude : envelope |x|
    """
    sig = samples[:max_points]
    t = np.arange(len(sig)) / sample_rate
    return {
        "times": t.tolist(),
        "i_values": sig.real.tolist(),
        "q_values": sig.imag.tolist(),
        "amplitude": np.abs(sig).tolist(),
    }
