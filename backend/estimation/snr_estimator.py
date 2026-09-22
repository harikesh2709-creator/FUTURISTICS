"""
SNR Estimator — M2M4 (second-and-fourth moment) estimator for
signal-to-noise ratio of digitally modulated signals.

Reference: D.R. Pauluzzi & N.C. Beaulieu, "A Comparison of SNR
Estimation Techniques for the AWGN Channel," IEEE Trans. Comm., 2000.
"""

import numpy as np


def estimate_snr_m2m4(
    samples: np.ndarray,
    modulation_order: int = 4,
    max_samples: int = 100000,
) -> dict:
    """
    Estimate SNR using the M2M4 method.

    Parameters
    ----------
    samples : complex baseband samples (should be power-normalized)
    modulation_order : modulation order M (2 for BPSK, 4 for QPSK, etc.)

    Returns dict:
        snr_db    : estimated SNR in dB
        snr_linear: linear SNR
        signal_power : estimated signal power
        noise_power  : estimated noise power
    """
    x = samples[:max_samples]
    x = x - np.mean(x)

    # Second and fourth moments of the envelope
    r = np.abs(x)
    M2 = np.mean(r ** 2)
    M4 = np.mean(r ** 4)

    # For constant-modulus signals (PSK), the kurtosis of the modulation
    # is kappa_a = 1. For QAM, kappa_a depends on constellation.
    # Using the general M2M4 estimator:
    #   M2 = S + N
    #   M4 = kappa_a * S^2 + 4*S*N + 2*N^2   (for circular complex Gaussian noise)
    #
    # Where S = signal power, N = noise power, kappa_a = E[|a|^4] / E[|a|^2]^2

    # Kurtosis of common constellations
    kurtosis_map = {
        2: 1.0,     # BPSK
        4: 1.0,     # QPSK (constant modulus)
        8: 1.0,     # 8-PSK
        16: 1.32,   # 16-QAM
        64: 1.381,  # 64-QAM
    }
    kappa_a = kurtosis_map.get(modulation_order, 1.0)

    # Solve quadratic for S:
    # M4 = kappa_a * S^2 + 4*S*(M2-S) + 2*(M2-S)^2
    # M4 = kappa_a * S^2 + 4*S*M2 - 4*S^2 + 2*M2^2 - 4*M2*S + 2*S^2
    # M4 = (kappa_a - 2) * S^2 + 2*M2^2
    # S^2 = (M4 - 2*M2^2) / (kappa_a - 2)

    denom = kappa_a - 2
    if abs(denom) < 1e-10:
        # Fallback for PSK (kappa_a ≈ 1, denom = -1)
        # For constant modulus: M4 = S^2 + 4SN + 2N^2 where M2 = S + N
        # Simplified: S^2 = 2*M2^2 - M4
        S_sq = 2 * M2 ** 2 - M4
    else:
        S_sq = (M4 - 2 * M2 ** 2) / denom

    if S_sq < 0:
        S_sq = abs(S_sq)  # Clamp for very low SNR

    S = np.sqrt(S_sq)
    N = M2 - S

    if N < 1e-12:
        N = 1e-12  # Prevent div by zero

    snr_lin = S / N
    snr_db = 10 * np.log10(snr_lin + 1e-30)

    return {
        "snr_db": round(float(snr_db), 2),
        "snr_linear": round(float(snr_lin), 4),
        "signal_power": round(float(S), 6),
        "noise_power": round(float(N), 6),
    }


def estimate_snr_spectral(
    samples: np.ndarray,
    sample_rate: float,
    signal_bw_fraction: float = 0.8,
    max_samples: int = 100000,
) -> dict:
    """
    Spectral SNR estimate: ratio of in-band power to out-of-band noise.

    This method estimates the noise floor from frequency bins outside the
    signal bandwidth, then computes signal power = total - noise.
    """
    from scipy.signal import welch

    sig = samples[:max_samples]
    f, Pxx = welch(sig, fs=sample_rate, nperseg=min(4096, len(sig)),
                   nfft=4096, return_onesided=False)
    f = np.fft.fftshift(f)
    Pxx = np.fft.fftshift(Pxx)

    total_power = np.sum(Pxx)

    # Estimate signal band from power centroid
    abs_f = np.abs(f)
    bw_cutoff = sample_rate * signal_bw_fraction / 2

    in_band = abs_f < bw_cutoff
    out_band = ~in_band

    if np.sum(out_band) < 10:
        return {"snr_db": 30.0, "snr_linear": 1000.0,
                "signal_power": float(total_power), "noise_power": 0.0}

    noise_floor_density = np.mean(Pxx[out_band])
    noise_power = noise_floor_density * len(Pxx)
    signal_power = total_power - noise_power

    if signal_power < 0:
        signal_power = total_power * 0.01
    if noise_power < 1e-12:
        noise_power = 1e-12

    snr_lin = signal_power / noise_power
    snr_db = 10 * np.log10(snr_lin)

    return {
        "snr_db": round(float(snr_db), 2),
        "snr_linear": round(float(snr_lin), 4),
        "signal_power": round(float(signal_power), 6),
        "noise_power": round(float(noise_power), 6),
    }
