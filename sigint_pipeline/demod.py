"""
demod.py
Coarse frequency correction, RRC matched filtering, Gardner timing
recovery, Costas-loop carrier recovery, and symbol slicing for
BPSK / QPSK. This targets linear PSK modulations end-to-end; QAM/FSK
share the same matched-filter + timing-recovery front end and would
plug in a different slicer (left as an extension point).
"""

import numpy as np


def rrc_filter(sps, span=8, beta=0.35):
    """Root-raised-cosine pulse, sps samples per symbol, `span` symbols long."""
    n = np.arange(-span * sps / 2, span * sps / 2 + 1)
    t = n / sps
    h = np.zeros_like(t)
    for i, ti in enumerate(t):
        if ti == 0:
            h[i] = (1 - beta + 4 * beta / np.pi)
        elif beta != 0 and abs(ti) == 1 / (4 * beta):
            h[i] = (beta / np.sqrt(2)) * (
                (1 + 2 / np.pi) * np.sin(np.pi / (4 * beta))
                + (1 - 2 / np.pi) * np.cos(np.pi / (4 * beta))
            )
        else:
            num = np.sin(np.pi * ti * (1 - beta)) + 4 * beta * ti * np.cos(
                np.pi * ti * (1 + beta)
            )
            den = np.pi * ti * (1 - (4 * beta * ti) ** 2)
            h[i] = num / den
    return (h / np.sqrt(np.sum(h ** 2))).astype(np.float32)


def coarse_freq_correct(iq, fs, order=2):
    """
    Estimate and remove a residual carrier offset by raising the signal
    to `order` (2 for BPSK, 4 for QPSK) to strip modulation, then finding
    the FFT peak, which sits at order * freq_offset.
    """
    raised = iq ** order
    spectrum = np.abs(np.fft.fft(raised))
    freqs = np.fft.fftfreq(len(raised), d=1 / fs)
    peak_idx = np.argmax(spectrum)
    offset = freqs[peak_idx] / order
    n = np.arange(len(iq))
    corrected = iq * np.exp(-1j * 2 * np.pi * offset * n / fs)
    return corrected.astype(np.complex64), float(offset)


def gardner_timing_recovery(x, sps):
    """
    Gardner timing-error-detector based symbol timing recovery.
    Operates at 2 samples/symbol internally for the TED; here we assume
    the input is already at (approximately) `sps` samples/symbol and
    resample-locks onto the correct decision instants.
    Returns the recovered symbol stream (one complex sample per symbol).
    """
    mu = 0.0          # fractional interpolation instant
    loop_gain = 0.01
    idx = int(sps)
    symbols = []

    # Simple linear interpolator over the float sample index.
    def interp(buf, pos):
        i0 = int(np.floor(pos))
        frac = pos - i0
        if i0 + 1 >= len(buf):
            return buf[-1]
        return buf[i0] * (1 - frac) + buf[i0 + 1] * frac

    pos = sps / 2.0
    step = sps
    last_sym = 0
    while True:
        mid_pos = pos - step / 2.0
        if int(np.ceil(pos)) >= len(x) or mid_pos < 0:
            break
        sample = interp(x, pos)
        mid = interp(x, mid_pos)
        symbols.append(sample)

        # Gardner error (real-valued TED on the real part is sufficient
        # for a first pass; extend to full complex TED for higher order).
        err = np.real(mid) * (np.real(sample) - last_sym)
        step = sps + loop_gain * np.clip(err, -1, 1) * sps * 0.1
        step = np.clip(step, sps * 0.9, sps * 1.1)
        last_sym = np.real(sample)
        pos += step

    return np.array(symbols, dtype=np.complex64)


def fixed_phase_symbol_sync(x, sps):
    """
    Robust non-iterative symbol timing recovery: after matched filtering,
    the correct sampling phase is the one that maximizes average symbol
    energy (ISI nulls out energy at wrong offsets). This is the default
    used by get_synced_symbols()/demodulate() -- it doesn't track sample
    clock DRIFT over a long capture the way a closed-loop TED would, but
    it locks reliably and is far less failure-prone for short/medium
    captures, which is what this prototype is tuned for. The Gardner
    loop above (gardner_timing_recovery) is kept as an extension point
    for long captures with real oscillator drift, where a closed loop is
    actually necessary -- swap it back in and tune loop_gain for that.
    """
    energies = [np.mean(np.abs(x[p::sps]) ** 2) for p in range(sps)]
    best_phase = int(np.argmax(energies))
    return x[best_phase::sps].astype(np.complex64), best_phase


def costas_loop(symbols, order=2, loop_bw=0.02):
    """
    Costas loop carrier phase tracking on the (already timing-recovered)
    symbol stream. order=2 for BPSK, order=4 for QPSK.
    """
    phase = 0.0
    freq = 0.0
    alpha = loop_bw
    beta_g = loop_bw ** 2 / 4
    out = np.zeros_like(symbols)

    for i, s in enumerate(symbols):
        corrected = s * np.exp(-1j * phase)
        out[i] = corrected

        if order == 2:
            error = np.real(corrected) * np.imag(corrected)
        else:  # order == 4, QPSK decision-directed error
            dec = np.sign(np.real(corrected)) + 1j * np.sign(np.imag(corrected))
            error = np.imag(corrected * np.conj(dec))

        freq += beta_g * error
        phase += freq + alpha * error

    return out


def get_synced_symbols(iq, fs, sps):
    """
    Coarse freq correction + matched filter + Gardner timing recovery,
    WITHOUT carrier phase lock or slicing. |C40|/|C42| cumulants are
    invariant to a *constant* residual phase rotation, but not to a
    time-varying one -- so an accurate frequency-offset removal matters
    here even though phase lock doesn't. order=4 is used because raising
    BPSK or QPSK to the 4th power both collapse the modulation to a pure
    tone at 4x the offset (order=2 only works for BPSK), which is why
    order=4 is the safer generic default before the modulation is known.
    The full demodulate() call below re-does freq correction at the
    modulation-appropriate order once the type is known.
    """
    corrected, offset_hz = coarse_freq_correct(iq, fs, order=4)
    h = rrc_filter(sps)
    filtered = np.convolve(corrected, h, mode="same").astype(np.complex64)
    symbols, _phase = fixed_phase_symbol_sync(filtered, sps)
    return symbols, offset_hz


def _mpsk_constellation(M):
    return np.exp(1j * 2 * np.pi * np.arange(M) / M)


def _qam16_constellation():
    levels = [-3, -1, 1, 3]
    pts = [complex(i, q) for i in levels for q in levels]
    return np.array(pts) / np.sqrt(10)  # unit average power


def _generic_nearest_point_slice(symbols, constellation, bits_per_symbol):
    """
    Fallback slicer for modulations without a dedicated fast-path
    (8PSK, 16QAM): nearest-constellation-point decision + index-to-bits.
    Lower fidelity than the dedicated BPSK/QPSK path above (no iterative
    carrier tracking tailored to the constellation order) -- adequate to
    keep the pipeline from crashing on a classifier hit for these types
    and a clear extension point for a full per-modulation slicer.
    """
    diffs = np.abs(symbols[:, None] - constellation[None, :])
    idx = np.argmin(diffs, axis=1)
    bits = np.zeros(len(symbols) * bits_per_symbol, dtype=np.uint8)
    for i, sym_idx in enumerate(idx):
        for b in range(bits_per_symbol):
            bits[i * bits_per_symbol + b] = (sym_idx >> (bits_per_symbol - 1 - b)) & 1
    return bits


def decision_directed_loop(symbols, constellation, loop_bw=0.02):
    """Generic decision-directed carrier tracking for any constellation
    (used for 8PSK / 16QAM, where the BPSK/QPSK-specific Costas error
    formula above doesn't apply)."""
    phase, freq = 0.0, 0.0
    alpha, beta_g = loop_bw, loop_bw ** 2 / 4
    out = np.zeros_like(symbols)
    for i, s in enumerate(symbols):
        corrected = s * np.exp(-1j * phase)
        out[i] = corrected
        idx = np.argmin(np.abs(corrected - constellation))
        decision = constellation[idx]
        error = np.imag(corrected * np.conj(decision))
        freq += beta_g * error
        phase += freq + alpha * error
    return out


def slice_symbols(symbols, modulation="BPSK"):
    """Map recovered symbols to bits (Gray-coded where applicable)."""
    if modulation == "BPSK":
        bits = (np.real(symbols) > 0).astype(np.uint8)
        return bits

    if modulation == "QPSK":
        i_bits = (np.real(symbols) > 0).astype(np.uint8)
        q_bits = (np.imag(symbols) > 0).astype(np.uint8)
        bits = np.empty(2 * len(symbols), dtype=np.uint8)
        bits[0::2] = i_bits
        bits[1::2] = q_bits
        return bits

    if modulation == "8PSK":
        return _generic_nearest_point_slice(symbols, _mpsk_constellation(8), 3)

    if modulation == "16QAM":
        return _generic_nearest_point_slice(symbols, _qam16_constellation(), 4)

    raise NotImplementedError(f"Slicer for {modulation} not implemented yet")


def demodulate(iq, fs, sps, modulation="BPSK"):
    """End-to-end: coarse freq correction -> matched filter -> timing
    recovery -> carrier tracking -> slicing -> bits."""
    freq_order = {"BPSK": 2, "QPSK": 4, "8PSK": 8, "16QAM": 4}.get(modulation, 4)
    corrected, offset_hz = coarse_freq_correct(iq, fs, order=freq_order)

    h = rrc_filter(sps)
    filtered = np.convolve(corrected, h, mode="same").astype(np.complex64)

    symbols, _phase = fixed_phase_symbol_sync(filtered, sps)

    if modulation in ("BPSK", "QPSK"):
        tracked = costas_loop(symbols, order=freq_order)
    elif modulation == "8PSK":
        tracked = decision_directed_loop(symbols, _mpsk_constellation(8))
    elif modulation == "16QAM":
        tracked = decision_directed_loop(symbols, _qam16_constellation())
    else:
        tracked = symbols

    bits = slice_symbols(tracked, modulation=modulation)
    return bits, {"freq_offset_hz": offset_hz, "n_symbols": len(symbols)}
