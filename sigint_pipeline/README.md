# SIGINT signal-analysis pipeline (prototype backend)

Working Python backend for the "automated .iq/.wav analysis and signal
parameter extraction" problem statement. This is the processing engine
a GUI would sit on top of -- every function here returns structured
data (not just prints) so it maps directly onto dashboard panels
(waterfall, constellation, classifier confidence bars, pipeline
stepper, parameter table, decode log).

## Quick start

```
pip install -r requirements.txt
python3 demo.py
```

`demo.py` generates a synthetic QPSK capture with **known** ground
truth (modulation, symbol rate, FEC code, interleave depth, sync
word), runs it through the full blind pipeline, and prints recovered
vs. true values side by side. On this test signal, everything is
currently recovered exactly:

```
modulation      truth=QPSK     recovered=QPSK
symbol rate     truth=4000.0   recovered=4000.0
interleave depth truth=8       recovered=8
sync-word hits: 1, best match: position=0, hamming_distance=0
```

To point it at a real capture instead:

```python
from pipeline import analyze
report, decoded_bits = analyze("capture.iq", sample_rate=2_048_000)
# or capture.wav, with sample rate read from the WAV header automatically
```

`report` is a dict with every extracted parameter, the classifier's
full ranking (not just top-1), the interleave-depth search table, and
a human-readable log list -- built for a GUI, not just a script.

## Module map

| File | Responsibility |
|---|---|
| `io_utils.py` | Load `.wav` / `.iq` into normalized complex64; `.iq` supports a JSON/SigMF-style sidecar for sample rate & center frequency, since raw `.iq` has no universal header |
| `characterize.py` | PSD, waterfall (spectrogram), occupied bandwidth, symbol-rate estimation (cyclostationary delay-and-multiply method), modulation classification via 4th-order cumulants (C40/C42, Swami & Sadler reference table) |
| `demod.py` | Coarse frequency correction, RRC matched filtering, symbol timing sync, Costas-loop / decision-directed carrier tracking, symbol slicing for BPSK/QPSK/8PSK/16QAM |
| `fec.py` | Convolutional encoder + hard-decision Viterbi decoder (K=7, rate 1/2, standard 171/133-octal generators) |
| `interleave.py` | Block interleaver/deinterleaver + depth search (tries candidate depths, scores each by re-encoding the decoded bits and measuring residual BER -- lowest wins) |
| `correlate.py` | Sync-word / preamble search over the decoded bitstream with a Hamming-distance tolerance, small library of known ASMs (CCSDS, HDLC flag) |
| `pipeline.py` | Orchestrates all of the above into one `analyze()` call and structured report |
| `siggen.py` | Synthetic test-signal generator with known ground truth -- the thing that makes this verifiable without a labeled real-world dataset |
| `demo.py` | Runs siggen -> pipeline -> ground-truth comparison |

## How parameter search works (the actual hard part)

Interleaving and FEC parameters aren't visible in the file -- the
pipeline can't know them a priori. Rather than guessing once, it uses
a **search-and-verify** loop: for interleaving, try each candidate
depth, Viterbi-decode the result, re-encode the decoded bits, and
measure how well the re-encoded bits match what was received. The
correct depth produces (near) zero residual error; wrong depths look
like random noise to the decoder and score badly. This is the same
principle the original proposal called for ("bit stream correlation
for identification") applied one layer earlier, to the parameters
themselves.

## What's implemented vs. extension points

**Implemented and verified end-to-end:**
- .wav / .iq loading with metadata sidecar
- PSD, waterfall, occupied bandwidth, symbol-rate estimation
- Modulation classification: BPSK / QPSK / 8PSK / 16QAM (cumulant-based)
- Demodulation: BPSK / QPSK (full Costas-loop carrier tracking), 8PSK /
  16QAM (decision-directed loop, functional but lower-fidelity slicer)
- FEC: convolutional K=7 r=1/2, hard-decision Viterbi
- Interleaving: block interleaver + blind depth search
- Bitstream correlation against known sync words

**Not yet implemented (flagged in the problem statement, left as clear
extension points with matching interfaces already in place):**
- FSK demodulation (needs a frequency discriminator front end, different
  from the PSK/QAM matched-filter path)
- Reed-Solomon / concatenated / LDPC decoders (`fec.py`'s `ConvCode` is
  one interchangeable decoder; a `RSCode` or `LDPCCode` class with the
  same `encode`/`decode` shape drops in the same way)
- Convolutional / diagonal / pseudo-random interleavers (same
  search-and-verify harness in `interleave.py` generalizes to them --
  block was implemented fully as the reference case)
- GUI layer (this backend's job was to make that layer trivial: every
  stage returns plottable/structured data already)

## Known limitations (real captures vs. synthetic test signal)

- Symbol timing sync currently uses a fixed-phase energy-maximization
  method (locks reliably, doesn't track slow clock drift across a long
  capture). A closed-loop Gardner timing-error detector is already
  written in `demod.py` (`gardner_timing_recovery`) as the upgrade path
  for long real-world captures with real oscillator drift -- it wasn't
  used as the default because for this deliverable it converged less
  reliably than the simpler fixed-phase method; needs loop-gain tuning
  before being the default.
- The classifier's reference cumulant table assumes roughly equiprobable
  symbols and a reasonable SNR; very low SNR or heavily filtered/real
  captures will need SNR-aware thresholds instead of nearest-neighbor
  matching.
