"""
run_analysis.py
CLI bridge for executing sigint_pipeline operations safely from external callers.
Outputs results as JSON to stdout.
"""

import sys
import os
import json
import argparse
import numpy as np

# Ensure sigint_pipeline directory is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pipeline
import interleave
import fec
import io_utils


def sanitize(obj):
    if isinstance(obj, dict):
        return {str(k): sanitize(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize(x) for x in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, complex):
        return {"real": float(obj.real), "imag": float(obj.imag)}
    return obj


def main():
    parser = argparse.ArgumentParser(description="SIGINT Pipeline Runner")
    parser.add_argument("--action", choices=["analyze", "depth-search"], default="analyze")
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--sample-rate", type=float, default=None)
    parser.add_argument("--mod-hint", type=str, default=None)
    parser.add_argument("--symbol-rate-hint", type=float, default=None)
    args = parser.parse_args()

    if args.action == "analyze":
        report, decoded_bits = pipeline.analyze(
            args.path,
            modulation_hint=args.mod_hint if args.mod_hint != "auto" else None,
            symbol_rate_hint=args.symbol_rate_hint,
            sample_rate=args.sample_rate,
        )
        output = {
            "status": "ok",
            "report": report,
            "decoded_bits_count": len(decoded_bits),
            "preview_bits": decoded_bits[:128].tolist(),
        }
        print(json.dumps(sanitize(output)))

    elif args.action == "depth-search":
        iq, meta = io_utils.load(args.path, sample_rate=args.sample_rate)
        fs = meta["sample_rate"]
        sr_est = pipeline.characterize.estimate_symbol_rate(iq, fs)
        sps = max(2, int(round(fs / (sr_est["symbol_rate_hz"] if sr_est else 4000))))
        bits, _ = pipeline.demod_mod.demodulate(iq, fs, sps, modulation=args.mod_hint or "QPSK")

        conv = fec.ConvCode()
        def score_fn(candidate_bits):
            sample = candidate_bits[:2048] if len(candidate_bits) > 2048 else candidate_bits
            decoded, info = conv.decode(sample)
            re_encoded = conv.encode(decoded)
            return fec.bit_error_rate(re_encoded, sample)

        candidate_depths = [d for d in range(2, 17) if len(bits) % d < d]
        best_depth, deinterleaved, depth_scores = interleave.search_deinterleave_depth(
            bits, candidate_depths, score_fn
        )
        output = {
            "status": "ok",
            "best_depth": best_depth,
            "depth_scores": depth_scores,
            "deinterleaved_bits": deinterleaved.tolist() if len(deinterleaved) > 0 else [],
        }
        print(json.dumps(sanitize(output)))


if __name__ == "__main__":
    main()
