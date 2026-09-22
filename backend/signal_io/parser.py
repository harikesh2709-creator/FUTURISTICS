"""
Signal I/O Parser — Multi-format .IQ and .wav file loader with automatic
format detection, IQ imbalance compensation, DC offset removal, and
normalization.

Supports:
  - WAV: PCM 8/16/24/32-bit int and 32-bit float, mono (real IF → analytic
    via Hilbert transform) and stereo (I = left, Q = right).
  - IQ:  Raw binary complex64 (interleaved float32), int16 (interleaved
    signed 16-bit), int8 (interleaved signed 8-bit).  Optional SigMF
    JSON sidecar for metadata (sample_rate, center_frequency, data_type).
"""

import json
import struct
import wave
from pathlib import Path
from typing import Optional

import numpy as np
from scipy.signal import hilbert


# ---------------------------------------------------------------------------
# Public data class returned by every loader
# ---------------------------------------------------------------------------
class SignalData:
    """Container for a loaded signal and its associated metadata."""

    def __init__(
        self,
        samples: np.ndarray,       # complex64 IQ array
        sample_rate: float,        # Hz
        center_freq: float = 0.0,  # Hz (0 = unknown / baseband)
        source_file: str = "",
        source_format: str = "",
        bit_depth: int = 0,
        num_channels: int = 1,
        duration_sec: float = 0.0,
    ):
        self.samples = samples
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.source_file = source_file
        self.source_format = source_format
        self.bit_depth = bit_depth
        self.num_channels = num_channels
        self.duration_sec = duration_sec if duration_sec else len(samples) / sample_rate

    def __repr__(self) -> str:
        return (
            f"SignalData({self.source_format}, "
            f"{len(self.samples)} samples, "
            f"Fs={self.sample_rate/1e3:.3f} kHz, "
            f"Fc={self.center_freq/1e6:.6f} MHz, "
            f"dur={self.duration_sec:.4f}s)"
        )


# ---------------------------------------------------------------------------
# IQ conditioning helpers
# ---------------------------------------------------------------------------
def remove_dc_offset(iq: np.ndarray) -> np.ndarray:
    """Remove DC bias from I and Q independently."""
    return iq - np.mean(iq)


def compensate_iq_imbalance(iq: np.ndarray) -> np.ndarray:
    """
    Simple amplitude-and-phase IQ imbalance compensation.
    Estimates gain imbalance g and phase skew φ from the signal statistics
    and applies the inverse affine transform.
    """
    I = iq.real.copy()
    Q = iq.imag.copy()

    # Estimate gain imbalance
    power_I = np.mean(I ** 2)
    power_Q = np.mean(Q ** 2)
    if power_I < 1e-12 or power_Q < 1e-12:
        return iq

    g = np.sqrt(power_Q / power_I)

    # Estimate phase skew from cross-correlation
    cross = np.mean(I * Q)
    sin_phi = 2.0 * cross / (np.sqrt(power_I) * np.sqrt(power_Q) + 1e-30)
    sin_phi = np.clip(sin_phi, -0.99, 0.99)
    cos_phi = np.sqrt(1.0 - sin_phi ** 2)

    # Correct
    I_corr = I
    Q_corr = (Q - g * sin_phi * I) / (g * cos_phi + 1e-30)

    return (I_corr + 1j * Q_corr).astype(np.complex64)


def normalize_power(iq: np.ndarray) -> np.ndarray:
    """Normalize to unit average power."""
    p = np.mean(np.abs(iq) ** 2)
    if p < 1e-12:
        return iq
    return (iq / np.sqrt(p)).astype(np.complex64)


def condition_signal(iq: np.ndarray) -> np.ndarray:
    """Apply full conditioning pipeline: DC removal → IQ comp → normalize."""
    iq = remove_dc_offset(iq)
    iq = compensate_iq_imbalance(iq)
    iq = normalize_power(iq)
    return iq


# ---------------------------------------------------------------------------
# WAV Loader
# ---------------------------------------------------------------------------
def load_wav(filepath: str, force_sample_rate: Optional[float] = None) -> SignalData:
    """
    Load a .wav file and return complex IQ samples.

    - Mono:   real IF signal → Hilbert transform to analytic signal.
    - Stereo: left channel = I, right channel = Q.
    """
    filepath = str(filepath)
    with wave.open(filepath, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()   # bytes per sample
        fs = wf.getframerate()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)

    if force_sample_rate is not None:
        fs = force_sample_rate

    bit_depth = sampwidth * 8

    # Decode PCM bytes → float64
    if sampwidth == 1:
        data = np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - 128.0
        data /= 128.0
    elif sampwidth == 2:
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
        data /= 32768.0
    elif sampwidth == 3:
        # 24-bit PCM: unpack manually
        total = len(raw) // 3
        data = np.zeros(total, dtype=np.float64)
        for i in range(total):
            b = raw[i * 3 : i * 3 + 3]
            val = struct.unpack_from("<i", b + (b"\x00" if b[2] < 128 else b"\xff"))[0]
            data[i] = val / 8388608.0
    elif sampwidth == 4:
        # Try int32 first, could be float32 in some non-standard wavs
        data = np.frombuffer(raw, dtype=np.int32).astype(np.float64)
        data /= 2147483648.0
    else:
        raise ValueError(f"Unsupported WAV sample width: {sampwidth} bytes")

    # Reshape for multi-channel
    if n_channels > 1:
        data = data.reshape(-1, n_channels)

    # Build complex IQ
    if n_channels >= 2:
        I = data[:, 0]
        Q = data[:, 1]
        iq = (I + 1j * Q).astype(np.complex64)
    else:
        # Mono → analytic via Hilbert
        analytic = hilbert(data)
        iq = analytic.astype(np.complex64)

    iq = condition_signal(iq)

    return SignalData(
        samples=iq,
        sample_rate=float(fs),
        center_freq=0.0,
        source_file=filepath,
        source_format="wav",
        bit_depth=bit_depth,
        num_channels=n_channels,
    )


# ---------------------------------------------------------------------------
# IQ Loader
# ---------------------------------------------------------------------------
_IQ_DTYPE_MAP = {
    "complex64": (np.complex64, 8),
    "cf32":      (np.complex64, 8),
    "cf32_le":   (np.complex64, 8),
    "int16":     (np.int16, 2),
    "ci16":      (np.int16, 2),
    "ci16_le":   (np.int16, 2),
    "int8":      (np.int8, 1),
    "ci8":       (np.int8, 1),
}


def _try_load_sigmf_meta(iq_path: str) -> dict:
    """Attempt to load a SigMF .sigmf-meta sidecar JSON file."""
    base = Path(iq_path)
    meta_path = base.with_suffix(".sigmf-meta")
    if not meta_path.exists():
        # Also try .json sidecar
        meta_path = base.with_suffix(".json")
    if not meta_path.exists():
        return {}

    try:
        with open(meta_path, "r") as f:
            meta = json.load(f)
        result = {}
        g = meta.get("global", meta)
        if "core:sample_rate" in g:
            result["sample_rate"] = float(g["core:sample_rate"])
        if "core:datatype" in g:
            result["data_type"] = g["core:datatype"]
        caps = meta.get("captures", [])
        if caps and "core:frequency" in caps[0]:
            result["center_freq"] = float(caps[0]["core:frequency"])
        return result
    except Exception:
        return {}


def load_iq(
    filepath: str,
    data_type: str = "complex64",
    sample_rate: float = 1.0e6,
    center_freq: float = 0.0,
) -> SignalData:
    """
    Load a raw binary .iq file.

    Parameters
    ----------
    filepath : path to .iq / .raw / .bin file
    data_type : one of complex64, int16, int8 (or SigMF aliases cf32, ci16, ci8)
    sample_rate : Hz — overridden by SigMF sidecar if present
    center_freq : Hz — overridden by SigMF sidecar if present
    """
    filepath = str(filepath)

    # Try SigMF metadata
    meta = _try_load_sigmf_meta(filepath)
    if "sample_rate" in meta:
        sample_rate = meta["sample_rate"]
    if "center_freq" in meta:
        center_freq = meta["center_freq"]
    if "data_type" in meta:
        data_type = meta["data_type"]

    dtype_key = data_type.lower().replace(" ", "").replace("-", "")
    if dtype_key not in _IQ_DTYPE_MAP:
        raise ValueError(
            f"Unknown IQ data type '{data_type}'. "
            f"Supported: {list(_IQ_DTYPE_MAP.keys())}"
        )

    np_dtype, bytes_per_component = _IQ_DTYPE_MAP[dtype_key]

    raw = np.fromfile(filepath, dtype=np_dtype)

    if np.iscomplexobj(raw):
        iq = raw.astype(np.complex64)
        bit_depth = bytes_per_component * 8 // 2  # per component
    else:
        # Interleaved I, Q, I, Q, ...
        if len(raw) % 2 != 0:
            raw = raw[:-1]  # Drop trailing byte
        I = raw[0::2].astype(np.float32)
        Q = raw[1::2].astype(np.float32)
        # Normalize integer types
        if np_dtype == np.int16:
            I /= 32768.0
            Q /= 32768.0
        elif np_dtype == np.int8:
            I /= 128.0
            Q /= 128.0
        iq = (I + 1j * Q).astype(np.complex64)
        bit_depth = bytes_per_component * 8

    iq = condition_signal(iq)

    return SignalData(
        samples=iq,
        sample_rate=sample_rate,
        center_freq=center_freq,
        source_file=filepath,
        source_format="iq",
        bit_depth=bit_depth,
        num_channels=2,
    )


# ---------------------------------------------------------------------------
# Auto-detect and load
# ---------------------------------------------------------------------------
def load_signal(
    filepath: str,
    iq_data_type: str = "complex64",
    iq_sample_rate: float = 1.0e6,
    iq_center_freq: float = 0.0,
    force_sample_rate: Optional[float] = None,
) -> SignalData:
    """
    Automatically detect file format and load.

    .wav files are parsed via the standard WAV header.
    .iq / .raw / .bin / .dat files are loaded as raw binary IQ.
    """
    p = Path(filepath)
    ext = p.suffix.lower()

    if ext in (".wav",):
        return load_wav(filepath, force_sample_rate=force_sample_rate)
    elif ext in (".iq", ".raw", ".bin", ".dat", ".cf32", ".cs16", ".cs8"):
        return load_iq(
            filepath,
            data_type=iq_data_type,
            sample_rate=iq_sample_rate,
            center_freq=iq_center_freq,
        )
    else:
        # Try WAV first, fall back to IQ
        try:
            return load_wav(filepath, force_sample_rate=force_sample_rate)
        except Exception:
            return load_iq(
                filepath,
                data_type=iq_data_type,
                sample_rate=iq_sample_rate,
                center_freq=iq_center_freq,
            )
