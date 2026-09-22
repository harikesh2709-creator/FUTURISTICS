"""
Root Raised Cosine (RRC) Matched Filter — Pulse shaping and matched
filtering for ISI-free symbol recovery in PSK / QAM systems.
"""

import numpy as np


def design_rrc_filter(
    num_taps: int = 101,
    samples_per_symbol: int = 4,
    alpha: float = 0.35,
) -> np.ndarray:
    """
    Design a Root Raised Cosine FIR filter.

    Parameters
    ----------
    num_taps : filter length (odd recommended)
    samples_per_symbol : oversampling factor
    alpha : roll-off factor (0 < alpha <= 1)

    Returns
    -------
    h : RRC impulse response, normalized to unit energy
    """
    T = float(samples_per_symbol)  # Symbol period in samples
    N = num_taps
    n = np.arange(N) - (N - 1) / 2  # Center at 0

    h = np.zeros(N)

    for i in range(N):
        t = n[i]
        if abs(t) < 1e-10:
            # t = 0
            h[i] = (1.0 / T) * (1.0 + alpha * (4.0 / np.pi - 1.0))
        elif alpha > 0 and abs(abs(t) - T / (4.0 * alpha)) < 1e-10:
            # t = ±T/(4α)
            h[i] = (alpha / (T * np.sqrt(2.0))) * (
                (1.0 + 2.0 / np.pi) * np.sin(np.pi / (4.0 * alpha))
                + (1.0 - 2.0 / np.pi) * np.cos(np.pi / (4.0 * alpha))
            )
        else:
            num = np.sin(np.pi * t / T * (1.0 - alpha)) + \
                  4.0 * alpha * (t / T) * np.cos(np.pi * t / T * (1.0 + alpha))
            den = np.pi * (t / T) * (1.0 - (4.0 * alpha * t / T) ** 2)
            if abs(den) < 1e-12:
                den = 1e-12
            h[i] = (1.0 / T) * num / den

    # Normalize to unit energy
    h /= np.sqrt(np.sum(h ** 2) + 1e-30)

    return h


def apply_matched_filter(
    samples: np.ndarray,
    samples_per_symbol: int = 4,
    alpha: float = 0.35,
    num_taps: int = 101,
) -> dict:
    """
    Apply RRC matched filter to the received signal.

    Returns dict:
        filtered : matched-filtered complex samples
        filter_h : the RRC impulse response used
    """
    h = design_rrc_filter(num_taps, samples_per_symbol, alpha)
    filtered = np.convolve(samples, h, mode="same").astype(np.complex64)

    return {
        "filtered": filtered,
        "filter_h": h,
    }
