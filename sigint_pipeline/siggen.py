"""
siggen.py
Builds a synthetic .iq test capture with KNOWN ground truth (modulation,
symbol rate, FEC code, interleaver depth, sync word) so the pipeline can
be verified end-to-end before pointing it at real, unlabeled captures.
"""

import numpy as np
from fec import ConvCode
from interleave import block_interleave
from demod import rrc_filter
from io_utils import save_iq
from correlate import KNOWN_SYNC_WORDS


def modulate(bits, modulation, sps):
    if modulation == "BPSK":
        symbols = 2.0 * bits.astype(np.float32) - 1.0
        symbols = symbols.astype(np.complex64)
    elif modulation == "QPSK":
        if len(bits) % 2 != 0:
            bits = bits[:-1]
        i = 2.0 * bits[0::2].astype(np.float32) - 1.0
        q = 2.0 * bits[1::2].astype(np.float32) - 1.0
        symbols = (i + 1j * q) / np.sqrt(2)
    else:
        raise NotImplementedError(modulation)

    upsampled = np.zeros(len(symbols) * sps, dtype=np.complex64)
    upsampled[::sps] = symbols
    h = rrc_filter(sps)
    shaped = np.convolve(upsampled, h, mode="same").astype(np.complex64)
    return shaped


def generate_test_capture(
    path,
    modulation="QPSK",
    fs=200_000.0,
    symbol_rate=4_000.0,
    freq_offset_hz=1200.0,
    snr_db=18.0,
    interleave_depth=8,
    n_payload_bits=2000,
    seed=42,
):
    rng = np.random.default_rng(seed)
    sps = int(round(fs / symbol_rate))

    sync = KNOWN_SYNC_WORDS["CCSDS_ASM"]
    sync_bits = np.array([int(c) for c in sync], dtype=np.uint8)
    payload_bits = rng.integers(0, 2, n_payload_bits, dtype=np.uint8)
    msg_bits = np.concatenate([sync_bits, payload_bits])

    conv = ConvCode()
    coded = conv.encode(msg_bits)

    interleaved, tail = block_interleave(coded, interleave_depth)
    tx_bits = np.concatenate([interleaved, tail])

    shaped = modulate(tx_bits, modulation, sps)

    n = np.arange(len(shaped))
    carrier = np.exp(1j * 2 * np.pi * freq_offset_hz * n / fs).astype(np.complex64)
    tx = shaped * carrier

    sig_power = np.mean(np.abs(tx) ** 2)
    noise_power = sig_power / (10 ** (snr_db / 10))
    noise = np.sqrt(noise_power / 2) * (
        rng.standard_normal(len(tx)) + 1j * rng.standard_normal(len(tx))
    )
    rx = (tx + noise).astype(np.complex64)

    save_iq(path, rx, sample_rate=fs, center_frequency=None)

    ground_truth = {
        "modulation": modulation,
        "sample_rate": fs,
        "symbol_rate": symbol_rate,
        "sps": sps,
        "freq_offset_hz": freq_offset_hz,
        "snr_db": snr_db,
        "conv_code": "K=7 r=1/2 (171,133 oct)",
        "interleave_depth": interleave_depth,
        "sync_word": sync,
        "n_msg_bits": len(msg_bits),
        "n_payload_bits": n_payload_bits,
    }
    return ground_truth
