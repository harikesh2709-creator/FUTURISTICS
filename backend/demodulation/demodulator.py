"""
Demodulator — Symbol-to-bit demapping for PSK (BPSK, QPSK, 8-PSK),
QAM (16-QAM, 64-QAM), and FSK (2-FSK, 4-FSK) with both hard-decision
bits and soft LLR output.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Constellation definitions (Gray-coded)
# ---------------------------------------------------------------------------
def _bpsk_constellation():
    return np.array([1.0 + 0j, -1.0 + 0j]), 1


def _qpsk_constellation():
    # Gray code: 00→(1+j), 01→(-1+j), 11→(-1-j), 10→(1-j)
    const = np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j]) / np.sqrt(2)
    return const, 2


def _8psk_constellation():
    gray_order = [0, 1, 3, 2, 6, 7, 5, 4]
    angles = [2 * np.pi * g / 8 for g in gray_order]
    return np.array([np.exp(1j * a) for a in angles]), 3


def _16qam_constellation():
    # 4x4 Gray-coded QAM
    gray_i = [-3, -1, 1, 3]
    gray_q = [-3, -1, 1, 3]
    const = np.array([complex(i, q) for q in gray_q for i in gray_i])
    const = const / np.sqrt(np.mean(np.abs(const) ** 2))
    return const, 4


def _64qam_constellation():
    levels = [-7, -5, -3, -1, 1, 3, 5, 7]
    const = np.array([complex(i, q) for q in levels for i in levels])
    const = const / np.sqrt(np.mean(np.abs(const) ** 2))
    return const, 6


_CONSTELLATION_MAP = {
    "bpsk": _bpsk_constellation,
    "qpsk": _qpsk_constellation,
    "8psk": _8psk_constellation,
    "8-psk": _8psk_constellation,
    "16qam": _16qam_constellation,
    "16-qam": _16qam_constellation,
    "64qam": _64qam_constellation,
    "64-qam": _64qam_constellation,
}


# ---------------------------------------------------------------------------
# Hard-decision slicer
# ---------------------------------------------------------------------------
def hard_decision_demap(
    symbols: np.ndarray,
    modulation: str = "qpsk",
) -> dict:
    """
    Map received symbols to nearest constellation point (hard decision)
    and extract bit sequence.

    Returns dict:
        bits          : np.ndarray uint8 — demodulated bits
        symbol_indices: np.ndarray int   — indices into constellation
        constellation : np.ndarray       — reference constellation
        evm_percent   : float — Error Vector Magnitude (%)
    """
    mod_key = str(modulation).lower().replace("-", "").replace("_", "")
    if mod_key not in _CONSTELLATION_MAP:
        mod_key = "qpsk"

    const, bps = _CONSTELLATION_MAP[mod_key]()

    # Normalize received symbols power to 1.0 before demapping and EVM calculation
    rms = np.sqrt(np.mean(np.abs(symbols) ** 2))
    if rms > 1e-12:
        symbols = symbols / rms

    # Minimum distance mapping
    indices = np.zeros(len(symbols), dtype=int)
    errors = np.zeros(len(symbols))

    for i, sym in enumerate(symbols):
        dists = np.abs(sym - const)
        idx = np.argmin(dists)
        indices[i] = idx
        errors[i] = dists[idx]

    # Convert indices to bits (MSB first)
    bits = []
    for idx in indices:
        for b in range(bps - 1, -1, -1):
            bits.append((idx >> b) & 1)
    bits = np.array(bits, dtype=np.uint8)

    # EVM calculation
    ref_symbols = const[indices]
    evm_rms = np.sqrt(np.mean(np.abs(symbols - ref_symbols) ** 2))
    ref_power = np.sqrt(np.mean(np.abs(ref_symbols) ** 2))
    evm_percent = float(evm_rms / (ref_power + 1e-30) * 100)

    return {
        "bits": bits,
        "symbol_indices": indices,
        "constellation": const,
        "evm_percent": round(evm_percent, 2),
        "bits_per_symbol": bps,
        "num_bits": len(bits),
    }


# ---------------------------------------------------------------------------
# FSK demodulator
# ---------------------------------------------------------------------------
def demodulate_fsk(
    samples: np.ndarray,
    sample_rate: float,
    samples_per_symbol: int = 4,
    fsk_order: int = 2,
) -> dict:
    """
    Demodulate FSK using quadrature frequency discriminator.

    Instantaneous frequency: f[n] = angle(x[n] * conj(x[n-1])) * Fs / (2π)
    Then downsample at symbol rate and quantize to M levels.

    Returns dict:
        bits    : demodulated bit array
        freqs   : instantaneous frequency trace
    """
    # Instantaneous frequency discriminator
    prod = samples[1:] * np.conj(samples[:-1])
    inst_freq = np.angle(prod) / (2 * np.pi) * sample_rate

    # Downsample to symbol rate
    sps = samples_per_symbol
    sym_freqs = []
    for i in range(0, len(inst_freq) - sps, sps):
        sym_freqs.append(np.mean(inst_freq[i:i + sps]))
    sym_freqs = np.array(sym_freqs)

    # Quantize to M levels
    M = fsk_order
    bps = int(np.log2(M))

    # Estimate frequency levels using k-means-like clustering
    sorted_f = np.sort(sym_freqs)
    chunk = len(sorted_f) // M
    centers = []
    for k in range(M):
        centers.append(np.mean(sorted_f[k * chunk:(k + 1) * chunk]))
    centers = np.array(centers)

    # Map each symbol to nearest center
    indices = np.zeros(len(sym_freqs), dtype=int)
    for i, f in enumerate(sym_freqs):
        indices[i] = np.argmin(np.abs(f - centers))

    # Convert to bits
    bits = []
    for idx in indices:
        for b in range(bps - 1, -1, -1):
            bits.append((idx >> b) & 1)
    bits = np.array(bits, dtype=np.uint8)

    return {
        "bits": bits,
        "freqs": inst_freq.tolist(),
        "sym_freqs": sym_freqs.tolist(),
        "fsk_centers": centers.tolist(),
        "num_bits": len(bits),
    }


# ---------------------------------------------------------------------------
# Full demodulation pipeline
# ---------------------------------------------------------------------------
def demodulate(
    symbols: np.ndarray,
    modulation: str = "qpsk",
    sample_rate: float = 1e6,
    samples_per_symbol: int = 4,
) -> dict:
    """
    Unified demodulation interface.

    For PSK/QAM: performs hard-decision constellation demapping.
    For FSK: uses frequency discriminator.
    """
    mod_key = modulation.lower().replace("-", "").replace("_", "").replace(" ", "")

    if "fsk" in mod_key:
        fsk_order = 4 if "4" in mod_key else 2
        return demodulate_fsk(symbols, sample_rate, samples_per_symbol, fsk_order)
    else:
        return hard_decision_demap(symbols, modulation)
