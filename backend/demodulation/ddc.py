"""
Digital Down-Conversion (DDC) — Frequency shifting, carrier offset
removal, and baseband conversion.
"""

import numpy as np


def frequency_shift(
    samples: np.ndarray,
    sample_rate: float,
    shift_hz: float,
) -> np.ndarray:
    """
    Shift signal by shift_hz (negative = shift left).
    x_shifted[n] = x[n] * exp(-j * 2π * f_shift * n / Fs)
    """
    n = np.arange(len(samples))
    return (samples * np.exp(-1j * 2 * np.pi * shift_hz * n / sample_rate)).astype(
        np.complex64
    )


def estimate_carrier_offset(
    samples: np.ndarray,
    sample_rate: float,
    nfft: int = 4096,
) -> float:
    """
    Estimate residual carrier frequency offset by finding the spectral
    peak of |X(f)|^2 (power centroid near the strongest component).
    """
    X = np.fft.fftshift(np.fft.fft(samples[:nfft], nfft))
    mag = np.abs(X) ** 2
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft, 1.0 / sample_rate))

    # Power centroid
    total = np.sum(mag)
    if total < 1e-30:
        return 0.0
    fc = float(np.sum(freqs * mag) / total)
    return fc


def digital_down_convert(
    samples: np.ndarray,
    sample_rate: float,
    carrier_freq: float = 0.0,
    auto_detect: bool = True,
) -> dict:
    """
    Perform digital down-conversion to baseband.

    If auto_detect is True, estimates and removes the carrier offset.

    Returns dict:
        samples        : baseband complex64 samples
        carrier_offset : detected/applied carrier offset in Hz
    """
    if auto_detect and carrier_freq == 0.0:
        carrier_freq = estimate_carrier_offset(samples, sample_rate)

    if abs(carrier_freq) > 1.0:  # More than 1 Hz offset
        baseband = frequency_shift(samples, sample_rate, carrier_freq)
    else:
        baseband = samples.copy()

    return {
        "samples": baseband,
        "carrier_offset": float(carrier_freq),
    }


def decimate(
    samples: np.ndarray,
    factor: int,
) -> np.ndarray:
    """Simple decimation by integer factor (no anti-alias filter)."""
    return samples[::factor]
