"""
demo.py
Generates a synthetic .iq capture with known ground truth, runs it
through the full pipeline, and prints a side-by-side comparison so you
can see the system correctly (or incorrectly) recovering each parameter.
Run: python3 demo.py
"""

from siggen import generate_test_capture
from pipeline import analyze
import fec as fec_mod

TEST_FILE = "test_capture.iq"


def main():
    print("=" * 70)
    print("STEP 1: generating synthetic test signal")
    print("=" * 70)
    truth = generate_test_capture(
        TEST_FILE,
        modulation="QPSK",
        fs=200_000.0,
        symbol_rate=4_000.0,
        freq_offset_hz=1200.0,
        snr_db=20.0,
        interleave_depth=8,
        n_payload_bits=2000,
    )
    for k, v in truth.items():
        print(f"  {k}: {v}")

    print()
    print("=" * 70)
    print("STEP 2: running blind analysis pipeline")
    print("=" * 70)
    report, decoded_bits = analyze(TEST_FILE, sample_rate=truth["sample_rate"])
    for line in report["log"]:
        print("  " + line)

    print()
    print("=" * 70)
    print("STEP 3: ground truth vs. recovered")
    print("=" * 70)
    print(f"  modulation      truth={truth['modulation']:<8} "
          f"recovered={report['modulation_used']}")
    print(f"  symbol rate     truth={truth['symbol_rate']:<8.1f} "
          f"recovered={report['symbol_rate_estimate']['symbol_rate_hz']:.1f}")
    print(f"  interleave depth truth={truth['interleave_depth']:<3} "
          f"recovered={report['interleave_depth_used']}")
    print(f"  sync-word hits: {len(report['sync_word_matches'])} "
          f"(expect >=1 near bitstream start)")
    if report["sync_word_matches"]:
        best = min(report["sync_word_matches"], key=lambda m: m["hamming_distance"])
        print(f"  best sync match: position={best['position']} "
              f"hamming_distance={best['hamming_distance']}")


if __name__ == "__main__":
    main()
