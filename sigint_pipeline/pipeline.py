"""
pipeline.py
Orchestrates the full chain and returns a structured report -- this is
the function a GUI layer would call per loaded file, and each stage's
output maps directly onto a dashboard panel (PSD/waterfall, classifier
confidence bars, pipeline stepper state, parameters table, decode log).
"""

import numpy as np
import io_utils
import characterize
import demod as demod_mod
import fec as fec_mod
import interleave as interleave_mod
import correlate as correlate_mod


def analyze(path, modulation_hint=None, symbol_rate_hint=None, sample_rate=None):
    log = []

    iq, meta = io_utils.load(path, sample_rate=sample_rate)
    fs = meta["sample_rate"]
    log.append(f"loaded {path} -- {len(iq)} samples @ {fs:.0f} Hz")

    bw_hz, center_hz = characterize.occupied_bandwidth(iq, fs)
    sr_est = characterize.estimate_symbol_rate(iq, fs)
    symbol_rate = symbol_rate_hint or (sr_est["symbol_rate_hz"] if sr_est else None)
    log.append(f"occupied bandwidth ~{bw_hz:.0f} Hz, symbol rate estimate "
                f"{symbol_rate:.1f} Bd (confidence {sr_est['confidence']:.2f})"
                if sr_est else "symbol rate estimate failed")

    if symbol_rate is None:
        raise RuntimeError("Could not estimate symbol rate; supply symbol_rate_hint.")
    sps = max(2, int(round(fs / symbol_rate)))

    # Classify on timing-recovered SYMBOLS, not the raw oversampled/pulse-
    # shaped waveform -- cumulant statistics assume symbol-rate sampling.
    synced_symbols, _ = demod_mod.get_synced_symbols(iq, fs, sps)
    ranked_mods, cumulant_stats = characterize.classify_modulation(synced_symbols)
    modulation = modulation_hint or ranked_mods[0][0]
    log.append(f"modulation classifier: {ranked_mods}")

    bits, demod_info = demod_mod.demodulate(iq, fs, sps, modulation=modulation)
    log.append(f"demodulated {len(bits)} bits, residual freq offset "
               f"{demod_info['freq_offset_hz']:.1f} Hz")

    conv = fec_mod.ConvCode()

    def score_fn(candidate_bits):
        decoded, info = conv.decode(candidate_bits)
        re_encoded = conv.encode(decoded)
        return fec_mod.bit_error_rate(re_encoded, candidate_bits)

    candidate_depths = [d for d in range(2, 17) if len(bits) % d < d]
    best_depth, deinterleaved, depth_scores = interleave_mod.search_deinterleave_depth(
        bits, candidate_depths, score_fn
    )
    log.append(f"interleaver depth search: best={best_depth}, "
               f"top candidates={depth_scores[:3]}")

    decoded_bits, decode_info = conv.decode(deinterleaved)
    log.append(f"Viterbi decode: {decode_info['n_symbols']} symbols, "
               f"path metric {decode_info['final_path_metric']:.0f}")

    sync_pattern = correlate_mod.KNOWN_SYNC_WORDS["CCSDS_ASM"]
    matches = correlate_mod.find_sync_word(decoded_bits, sync_pattern, max_hamming=3)
    log.append(f"sync-word correlation: {len(matches)} candidate hit(s)")

    report = {
        "file": path,
        "sample_rate_hz": fs,
        "occupied_bandwidth_hz": bw_hz,
        "center_offset_hz": center_hz,
        "symbol_rate_estimate": sr_est,
        "modulation_ranking": ranked_mods,
        "modulation_used": modulation,
        "cumulant_stats": cumulant_stats,
        "n_demod_bits": len(bits),
        "interleave_depth_used": best_depth,
        "interleave_depth_scores": depth_scores,
        "decode_path_metric": decode_info["final_path_metric"],
        "sync_word_matches": matches,
        "decoded_bits_preview": decoded_bits[:64].tolist(),
        "log": log,
    }
    return report, decoded_bits


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "test_capture.iq"
    report, decoded = analyze(path)
    for line in report["log"]:
        print(line)
