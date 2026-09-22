"""
Synchronization — Gardner timing error detector for symbol clock recovery
and Costas loop for carrier phase tracking.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Gardner Timing Error Detector & Symbol Clock Recovery
# ---------------------------------------------------------------------------
def gardner_timing_recovery(
    samples: np.ndarray,
    samples_per_symbol: int = 4,
    loop_bw: float = 0.01,
    damping: float = 0.707,
    max_symbols: int = 0,
) -> dict:
    """
    Gardner timing error detector (TED) with proportional-integral loop
    filter for symbol clock recovery.

    TED:  e[k] = Re{x[kT+T/2] * conj(x[kT] - x[(k-1)T])}

    Parameters
    ----------
    samples : matched-filtered complex samples
    samples_per_symbol : nominal oversampling factor
    loop_bw : normalized loop bandwidth (0 < bw < 0.1)
    damping : loop damping factor (ζ)

    Returns dict:
        symbols      : recovered symbol samples (complex)
        timing_error : timing error signal
        mu_history   : fractional delay history
    """
    sps = float(samples_per_symbol)

    # PI loop filter gains (from loop bandwidth and damping)
    theta = loop_bw / (damping + 1.0 / (4.0 * damping))
    K1 = 4 * damping * theta / (1 + 2 * damping * theta + theta ** 2)
    K2 = 4 * theta ** 2 / (1 + 2 * damping * theta + theta ** 2)

    N = len(samples)
    if max_symbols > 0:
        max_out = max_symbols
    else:
        max_out = int(N / sps) + 100

    symbols = np.zeros(max_out, dtype=np.complex64)
    timing_errors = np.zeros(max_out)
    mu_history = np.zeros(max_out)

    mu = 0.0       # Fractional delay (0 <= mu < 1)
    idx = int(sps)  # Current sample index
    cnt = 0         # Output symbol count
    prev_symbol = 0 + 0j
    integrator = 0.0

    while idx < N - int(sps) - 2 and cnt < max_out:
        # Interpolate at idx + mu using linear interpolation
        i0 = int(idx)
        frac = mu
        if i0 + 1 < N:
            x_sym = samples[i0] * (1 - frac) + samples[i0 + 1] * frac
        else:
            break

        # Mid-point sample (T/2 before current symbol)
        mid_idx = int(idx - sps / 2)
        mid_frac = mu
        if 0 <= mid_idx < N - 1:
            x_mid = samples[mid_idx] * (1 - mid_frac) + samples[mid_idx + 1] * mid_frac
        else:
            x_mid = 0

        # Gardner TED
        e = float(np.real(x_mid * np.conj(x_sym - prev_symbol)))
        timing_errors[cnt] = e

        # PI loop filter
        integrator += K2 * e
        w = K1 * e + integrator

        # Update timing
        mu += w
        idx += int(sps + mu)
        mu = mu - int(mu)  # Keep fractional part
        if mu < 0:
            mu += 1
            idx -= 1

        mu_history[cnt] = mu
        symbols[cnt] = x_sym
        prev_symbol = x_sym
        cnt += 1

    symbols = symbols[:cnt]
    timing_errors = timing_errors[:cnt]
    mu_history = mu_history[:cnt]

    return {
        "symbols": symbols,
        "timing_error": timing_errors.tolist(),
        "mu_history": mu_history.tolist(),
        "num_symbols": cnt,
    }


# ---------------------------------------------------------------------------
# Costas Loop — Carrier Phase Recovery
# ---------------------------------------------------------------------------
def costas_loop(
    symbols: np.ndarray,
    modulation_order: int = 4,
    loop_bw: float = 0.005,
    damping: float = 0.707,
) -> dict:
    """
    M-th power Costas loop for carrier phase recovery.

    For QPSK (M=4): raises signal to 4th power to remove modulation,
    then tracks the residual phase with a PLL.

    Parameters
    ----------
    symbols : complex symbol samples (after timing recovery)
    modulation_order : M (2=BPSK, 4=QPSK, 8=8PSK)
    loop_bw : normalized loop bandwidth
    damping : damping factor

    Returns dict:
        corrected : phase-corrected symbols
        phase     : tracked phase history
    """
    M = modulation_order

    # PI gains
    theta = loop_bw / (damping + 1.0 / (4.0 * damping))
    K1 = 4 * damping * theta / (1 + 2 * damping * theta + theta ** 2)
    K2 = 4 * theta ** 2 / (1 + 2 * damping * theta + theta ** 2)

    N = len(symbols)
    corrected = np.zeros(N, dtype=np.complex64)
    phase_history = np.zeros(N)

    phase = 0.0
    freq = 0.0

    for i in range(N):
        # De-rotate by current phase estimate
        corrected[i] = symbols[i] * np.exp(-1j * phase)

        # Phase error detector (M-th power)
        if M == 2:
            # BPSK: error = Im(x^2)
            err = float(np.imag(corrected[i] ** 2))
        elif M == 4:
            # QPSK: error = Im(x^4) / 4
            err = float(np.imag(corrected[i] ** 4)) / 4.0
        elif M == 8:
            # 8PSK: error = Im(x^8) / 8
            err = float(np.imag(corrected[i] ** 8)) / 8.0
        else:
            # Decision-directed for QAM
            # Quantize to nearest constellation point
            re = np.sign(corrected[i].real)
            im = np.sign(corrected[i].imag)
            ref = complex(re, im)
            err = float(np.imag(corrected[i] * np.conj(ref)))

        # PI loop filter
        freq += K2 * err
        phase += K1 * err + freq
        phase_history[i] = phase

    return {
        "corrected": corrected,
        "phase": phase_history.tolist(),
    }


def full_sync_pipeline(
    samples: np.ndarray,
    samples_per_symbol: int = 4,
    modulation_order: int = 4,
    timing_bw: float = 0.01,
    carrier_bw: float = 0.005,
) -> dict:
    """
    Full synchronization pipeline: Gardner TED → Costas carrier recovery.

    Returns dict with all intermediate and final results.
    """
    # Step 1: Symbol timing recovery
    timing_result = gardner_timing_recovery(
        samples, samples_per_symbol, loop_bw=timing_bw
    )

    # Step 2: Carrier phase recovery
    carrier_result = costas_loop(
        timing_result["symbols"],
        modulation_order=modulation_order,
        loop_bw=carrier_bw,
    )

    return {
        "symbols_raw": timing_result["symbols"],
        "symbols_synced": carrier_result["corrected"],
        "timing_error": timing_result["timing_error"],
        "carrier_phase": carrier_result["phase"],
        "num_symbols": timing_result["num_symbols"],
    }
