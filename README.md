# NTRO 26147 - Signal Analyzer

Automated Model for Analysis of .IQ and .wav Files along with signal parameter extraction.
Developed for the National Technical Research Organisation (NTRO) Problem Statement 26147 (Space Technology).

## Features

- **Ingestion**: Supports `.IQ` and `.wav` formats with I/Q DC offset calibration.
- **Spectral Analysis**: High-performance FFT, Welch PSD, Waterfall/Spectrogram, and Occupied Bandwidth (OBW) estimation.
- **Parameter Extraction**: 
  - Symbol Rate (Baud) estimation using cyclostationary & squaring techniques.
  - Signal-to-Noise Ratio (SNR) estimation using M2M4 and spectral methods.
  - Automatic Modulation Classification (AMC) using Higher-Order Cumulants.
- **Demodulation Pipeline**: Digital Down Conversion (DDC), RRC filtering, Gardner Timing Error Detection, Costas Loop Carrier Recovery, and Bit Demapping.
- **Interleaving & FEC**: 
  - Blind interleaver parameter estimation.
  - Convolutional (Viterbi), Reed-Solomon (CCSDS/DVB), Concatenated, and LDPC decoding.
- **Framing & Correlation**: Sliding bitstream correlator for Sync word detection, frame parsing, CRC verification, and bitstream entropy.
- **Tactical Dashboard**: Aerospace-grade dark mode Web UI built with FastAPI & Canvas for real-time visualization.

## Getting Started

### Prerequisites

- Python 3.9+
- `pip install numpy scipy fastapi uvicorn python-multipart`

### Running the Server

Start the analyzer by running the launcher script:

```bash
python run_server.py
```

Open your browser to `http://localhost:8000`.

### Using the Application

1. **Upload Signal**: Use the `SIGNAL INPUT` section to load a `.IQ` or `.wav` file, or generate a synthetic signal to test the pipeline.
2. **Auto-Analyze**: Click `Auto-Analyze Signal` to compute spectral density, spectrogram, and perform modulation & baud rate estimation.
3. **Demodulation**: Configure parameters and click `Demodulate` to view the raw and synchronized Constellation/Eye diagrams.
4. **De-interleave & FEC**: Run `De-interleave` and select a `FEC` type (e.g. Viterbi, RS, Concatenated, LDPC) to decode the bitstream.
5. **Correlation**: Select a Sync Pattern (e.g. CCSDS ASM) and hit `Correlate & Frame` to view bitstream payload dumps and frame parsing results.

## Architecture

- **Backend**: `FastAPI` (Orchestrator) + `numpy`/`scipy` (DSP Engine). No heavy dependencies like PyTorch/GNU Radio. Custom implementations for Viterbi, Galois Fields, and LDPC.
- **Frontend**: Vanilla HTML/JS with HTML5 Canvas renderers for low-latency spectrograms and constellations.

## Directory Structure

- `backend/`: Core signal processing modules.
  - `signal_io/`: File parsing and synthetic generation.
  - `spectral/`: FFT, PSD, Spectrogram.
  - `estimation/`: AMC, Baud, SNR.
  - `demodulation/`: DDC, matched filtering, synchronization.
  - `interleaving/`: Blind detection and deinterleaving.
  - `fec/`: Viterbi, Reed-Solomon, Concatenated, LDPC.
  - `correlation/`: Sync word detection and parsing.
- `frontend/`: Web UI static assets.
- `sample_data/`: Directory where synthetic signals are saved.
- `run_server.py`: Server entrypoint.

## License
Proprietary / Restricted for NTRO.
