"""
io_utils.py
Load/save .wav and .iq captures into a normalized complex64 numpy array,
along with a metadata dict (sample_rate, center_freq if known).

.iq files have no universal standard, so we support:
  - raw interleaved float32 I/Q  (default assumption)
  - raw interleaved int16 I/Q    (set dtype='int16')
  - a JSON sidecar "<name>.sigmf-meta" or "<name>.json" describing the format,
    following a reduced SigMF-like schema:
      {
        "sample_rate": 2048000,
        "center_frequency": 14200000,
        "dtype": "cf32" | "ci16",
        "channels": "interleaved_iq"
      }
"""

import json
import os
import numpy as np
import wave


def _find_sidecar(iq_path):
    for ext in (".sigmf-meta", ".json"):
        candidate = os.path.splitext(iq_path)[0] + ext
        if os.path.exists(candidate):
            with open(candidate, "r") as f:
                return json.load(f)
    return None


def load_iq(path, sample_rate=None, dtype="float32"):
    """
    Load a raw .iq file into a complex64 numpy array.

    path: path to the .iq file
    sample_rate: override sample rate (Hz). If None, looked up from sidecar,
                 else raises unless the caller supplies one.
    dtype: 'float32' or 'int16' -- underlying storage type of I/Q samples.
    """
    meta = _find_sidecar(path) or {}
    fs = sample_rate or meta.get("sample_rate")
    dt = meta.get("dtype", dtype)

    raw = np.fromfile(path, dtype=np.float32 if dt in ("float32", "cf32") else np.int16)
    if raw.size % 2 != 0:
        raw = raw[:-1]  # drop a stray trailing sample
    iq = raw[0::2].astype(np.float32) + 1j * raw[1::2].astype(np.float32)

    if dt in ("int16", "ci16"):
        iq = iq / 32768.0  # normalize to [-1, 1]

    if fs is None:
        raise ValueError(
            f"No sample_rate found for {path}. Provide sample_rate= or a "
            f"sidecar {os.path.splitext(path)[0]}.json with a 'sample_rate' field."
        )

    return iq.astype(np.complex64), {
        "sample_rate": float(fs),
        "center_frequency": meta.get("center_frequency"),
        "source": path,
    }


def load_wav(path):
    """
    Load a .wav file. Mono -> real signal (returned as complex with zero
    imaginary part, since some downstream stages expect complex input).
    Stereo -> treated as interleaved I/Q (channel 0 = I, channel 1 = Q),
    which is a common convention for SDR audio-rate recordings.
    """
    with wave.open(path, "rb") as wf:
        n_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        fs = wf.getframerate()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)

    dtype_map = {1: np.uint8, 2: np.int16, 4: np.int32}
    dt = dtype_map.get(sample_width, np.int16)
    data = np.frombuffer(raw, dtype=dt).astype(np.float32)

    if sample_width == 2:
        data /= 32768.0
    elif sample_width == 4:
        data /= 2147483648.0
    elif sample_width == 1:
        data = (data - 128.0) / 128.0

    if n_channels == 2:
        data = data.reshape(-1, 2)
        iq = data[:, 0] + 1j * data[:, 1]
    else:
        iq = data.astype(np.complex64)

    return iq.astype(np.complex64), {
        "sample_rate": float(fs),
        "center_frequency": None,
        "source": path,
    }


def load(path, **kwargs):
    """Dispatch on file extension."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".wav":
        return load_wav(path)
    elif ext in (".iq", ".bin", ".dat"):
        return load_iq(path, **kwargs)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def save_iq(path, iq, sample_rate, center_frequency=None):
    """Save a complex64 array as raw interleaved float32 .iq plus JSON sidecar."""
    interleaved = np.empty(iq.size * 2, dtype=np.float32)
    interleaved[0::2] = iq.real
    interleaved[1::2] = iq.imag
    interleaved.tofile(path)

    meta = {
        "sample_rate": sample_rate,
        "center_frequency": center_frequency,
        "dtype": "cf32",
        "channels": "interleaved_iq",
    }
    with open(os.path.splitext(path)[0] + ".json", "w") as f:
        json.dump(meta, f, indent=2)
