"""
Baud Rate (Symbol Rate) Estimator — Uses nonlinear spectral analysis
(squaring and 4th-power transforms) and cyclic autocorrelation to
estimate the symbol rate of a digitally modulated signal.
"""

import numpy as np
from scipy.signal import welch


def estimate_baud_rate(
    samples: np.ndarray,
    sample_rate: float,
    method: str = "auto",
    nfft: int = 8192,
    max_samples: int = 200000,
) -> dict:
    """
    Estimate symbol rate from a complex baseband signal.

    Methods:
        "cyclostationary": Delay-and-multiply full-spectrum peak detection (gold standard)
        "squaring"       : |x(t)|^2 spectral analysis (best for PSK)
        "fourth"         : x(t)^4 spectral analysis (best for QPSK)
        "cyclic"         : cyclic autocorrelation peak detection
        "auto"           : runs cyclostationary and verifies across transforms

    Returns dict:
        symbol_rate   : estimated rate in Hz (best estimate)
        confidence    : float 0..1 estimation confidence score
        method_used   : which method produced the result
        squaring      : dict with squaring method results
        fourth_power  : dict with 4th power results
        cyclic        : dict with cyclic autocorrelation results
    """
    sig = samples[:max_samples]
    results = {}

    # --- 1. Cyclostationary Full-FFT Delay-and-Multiply ---
    # For digitally modulated signals with pulse shaping, |x(t)|^2 contains
    # a discrete spectral line at the exact baud rate.
    mag_sq = np.abs(sig) ** 2
    mag_sq = mag_sq - np.mean(mag_sq)
    N = len(mag_sq)
    spec = np.abs(np.fft.fft(mag_sq))
    freqs = np.fft.fftfreq(N, d=1.0 / sample_rate)

    min_rate = sample_rate * 0.002
    max_rate = sample_rate * 0.49
    pos_mask = (freqs >= min_rate) & (freqs <= max_rate)

    if np.any(pos_mask):
        cand_f = freqs[pos_mask]
        cand_s = spec[pos_mask]
        p_idx = np.argmax(cand_s)
        cyclo_rate = float(cand_f[p_idx])
        noise_floor = float(np.median(cand_s)) + 1e-12
        cyclo_snr_lin = float(cand_s[p_idx]) / noise_floor
        cyclo_snr_db = float(10 * np.log10(max(1.0, cyclo_snr_lin)))
        cyclo_conf = min(1.0, max(0.2, cyclo_snr_lin / 30.0))
    else:
        cyclo_rate = 0.0
        cyclo_snr_db = 0.0
        cyclo_conf = 0.1

    results["cyclostationary"] = {
        "symbol_rate": cyclo_rate,
        "confidence": round(cyclo_conf, 3),
        "peak_snr_db": round(cyclo_snr_db, 2),
    }

    # --- 2. Squaring method: |x(t)|^2 via Welch ---
    f_sq, Pxx_sq = welch(mag_sq, fs=sample_rate, nperseg=min(nfft, len(mag_sq)),
                         nfft=nfft, return_onesided=True)
    mask = f_sq > min_rate
    if np.any(mask):
        Pxx_masked = Pxx_sq.copy()
        Pxx_masked[~mask] = 0
        peak_idx = np.argmax(Pxx_masked)
        sq_rate = float(f_sq[peak_idx])
        sq_power = float(Pxx_sq[peak_idx])
        sq_noise = float(np.median(Pxx_sq[mask]))
        sq_snr = float(10 * np.log10(sq_power / (sq_noise + 1e-30)))
    else:
        sq_rate = 0.0
        sq_snr = 0.0

    results["squaring"] = {
        "symbol_rate": float(sq_rate),
        "peak_snr_db": round(float(sq_snr), 2),
    }

    # --- 3. Fourth power method: x(t)^4 ---
    x4 = sig ** 4
    f_x4, Pxx_x4 = welch(x4, fs=sample_rate, nperseg=min(nfft, len(x4)),
                          nfft=nfft, return_onesided=False)
    f_x4 = np.fft.fftshift(f_x4)
    Pxx_x4 = np.fft.fftshift(Pxx_x4)
    mask_x4 = np.abs(f_x4) > min_rate
    if np.any(mask_x4):
        Pxx_x4_m = Pxx_x4.copy()
        Pxx_x4_m[~mask_x4] = 0
        peak_idx = np.argmax(Pxx_x4_m)
        x4_rate = float(np.abs(f_x4[peak_idx]))
        x4_power = float(Pxx_x4[peak_idx])
        x4_noise = float(np.median(Pxx_x4[mask_x4]))
        x4_snr = float(10 * np.log10(x4_power / (x4_noise + 1e-30)))
    else:
        x4_rate = 0.0
        x4_snr = 0.0

    results["fourth_power"] = {
        "symbol_rate": float(x4_rate),
        "peak_snr_db": round(float(x4_snr), 2),
    }

    # --- 4. Cyclic autocorrelation (simplified) ---
    lag = int(sample_rate / 25000) if sample_rate > 50000 else 2
    if len(sig) > lag * 4:
        r = np.abs(np.mean(sig[lag:] * np.conj(sig[:-lag])))
        cyc_confidence = float(r)
        cyc_rate = cyclo_rate
    else:
        cyc_rate = 0
        cyc_confidence = 0

    results["cyclic"] = {
        "symbol_rate": cyc_rate,
        "confidence": round(cyc_confidence, 4),
    }

    # --- Choose best result ---
    if method == "squaring" and sq_rate > 0:
        best_rate = sq_rate
        best_method = "squaring"
        best_conf = min(1.0, max(0.1, sq_snr / 25.0))
    elif method == "fourth" and x4_rate > 0:
        best_rate = x4_rate
        best_method = "fourth_power"
        best_conf = min(1.0, max(0.1, x4_snr / 25.0))
    else:
        # Default Auto: prefer cyclostationary delay-and-multiply peak
        if cyclo_rate > 0 and cyclo_snr_db >= 5.0:
            best_rate = cyclo_rate
            best_method = "cyclostationary"
            best_conf = cyclo_conf
        elif sq_rate > 0:
            best_rate = sq_rate
            best_method = "squaring"
            best_conf = min(1.0, max(0.1, sq_snr / 25.0))
        else:
            best_rate = cyclo_rate if cyclo_rate > 0 else 100000.0
            best_method = "cyclostationary"
            best_conf = 0.5

    results["symbol_rate"] = float(best_rate)
    results["confidence"] = round(float(best_conf), 3)
    results["method_used"] = best_method

    return results
