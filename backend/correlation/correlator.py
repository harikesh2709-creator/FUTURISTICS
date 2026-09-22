"""
Bitstream Correlator — Sliding cross-correlation for sync word detection
with Hamming distance tolerance. Supports standard sync patterns:
  - Barker codes (7, 11, 13)
  - CCSDS ASM (0x1ACFFC1D)
  - DVB Sync Byte (0x47)
  - Custom user-specified patterns
"""

import numpy as np


# ---------------------------------------------------------------------------
# Standard sync patterns
# ---------------------------------------------------------------------------
_SYNC_PATTERNS = {
    "barker7": np.array([1, 1, 1, 0, 0, 1, 0], dtype=np.uint8),
    "barker11": np.array([1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0], dtype=np.uint8),
    "barker13": np.array([1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1], dtype=np.uint8),
}


def _hex_to_bits(hex_str: str) -> np.ndarray:
    """Convert hex string to bit array."""
    hex_str = hex_str.replace("0x", "").replace(" ", "")
    byte_arr = bytes.fromhex(hex_str)
    return np.unpackbits(np.frombuffer(byte_arr, dtype=np.uint8))


def get_sync_pattern(name: str) -> np.ndarray:
    """
    Get a standard sync pattern by name.

    Names: "barker7", "barker11", "barker13", "ccsds_asm", "dvb_sync",
           or a hex string like "1ACFFC1D".
    """
    key = name.lower().replace("-", "").replace("_", "").replace(" ", "")

    if key in _SYNC_PATTERNS:
        return _SYNC_PATTERNS[key]
    elif key in ("ccsdsasm", "ccsds", "asm"):
        return _hex_to_bits("1ACFFC1D")
    elif key in ("dvbsync", "dvb", "0x47"):
        return _hex_to_bits("47")
    else:
        # Try parsing as hex
        try:
            return _hex_to_bits(name)
        except Exception:
            raise ValueError(f"Unknown sync pattern: {name}")


# ---------------------------------------------------------------------------
# Sliding correlator
# ---------------------------------------------------------------------------
def correlate_sync(
    bits: np.ndarray,
    sync_pattern: np.ndarray = None,
    sync_name: str = "ccsds_asm",
    hamming_threshold: int = 3,
    min_frame_spacing: int = 0,
) -> dict:
    """
    Sliding cross-correlation of bitstream against sync pattern.

    Parameters
    ----------
    bits : input bit array (uint8, 0 or 1)
    sync_pattern : explicit sync pattern (overrides sync_name)
    sync_name : name of standard sync pattern
    hamming_threshold : max allowed Hamming distance for a match
    min_frame_spacing : minimum bits between consecutive detections

    Returns dict:
        positions     : list of bit positions where sync was detected
        distances     : Hamming distances at each detection
        correlation   : full correlation trace (for plotting)
        sync_length   : length of sync pattern used
        num_detections: number of sync words found
    """
    if sync_pattern is None:
        sync_pattern = get_sync_pattern(sync_name)

    sync_len = len(sync_pattern)
    N = len(bits)

    if N < sync_len:
        return {
            "positions": [], "distances": [],
            "correlation": [], "sync_length": sync_len,
            "num_detections": 0,
        }

    # Compute sliding Hamming distance
    n_positions = N - sync_len + 1
    hamming = np.zeros(n_positions, dtype=np.int32)

    for i in range(n_positions):
        window = bits[i : i + sync_len]
        hamming[i] = np.sum(window != sync_pattern)

    # Normalized correlation (1 - hamming/sync_len)
    correlation = 1.0 - hamming.astype(float) / sync_len

    # Find detections below threshold
    positions = []
    distances = []
    last_pos = -min_frame_spacing - 1

    for i in range(n_positions):
        if hamming[i] <= hamming_threshold:
            if i - last_pos >= min_frame_spacing or not positions:
                positions.append(int(i))
                distances.append(int(hamming[i]))
                last_pos = i

    return {
        "positions": positions,
        "distances": distances,
        "correlation": correlation.tolist(),
        "sync_length": sync_len,
        "num_detections": len(positions),
    }


def auto_detect_frame_length(positions: list) -> dict:
    """
    Estimate frame length from detected sync positions.

    Returns dict:
        frame_length : estimated frame length in bits
        confidence   : detection confidence
        spacings     : list of inter-frame spacings
    """
    if len(positions) < 2:
        return {"frame_length": 0, "confidence": 0, "spacings": []}

    spacings = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]

    if not spacings:
        return {"frame_length": 0, "confidence": 0, "spacings": []}

    # Most common spacing (mode)
    from collections import Counter
    counts = Counter(spacings)
    frame_length, max_count = counts.most_common(1)[0]

    confidence = max_count / len(spacings)

    return {
        "frame_length": frame_length,
        "confidence": round(confidence, 3),
        "spacings": spacings,
    }
