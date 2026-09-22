"""
correlate.py
Slide a known sync-word/preamble pattern across a decoded bitstream and
report match positions, tolerating some bit errors (Hamming distance
threshold) since real decoded streams are rarely error-free.
"""

import numpy as np

# A small library of common sync words / attached sync markers (ASM).
KNOWN_SYNC_WORDS = {
    "CCSDS_ASM": "00011010110011111111110000011101",  # 0x1ACFFC1D
    "HDLC_FLAG_x8": "01111110" * 8,
}


def find_sync_word(bits, pattern_bits, max_hamming=2):
    """
    bits: np.ndarray of 0/1
    pattern_bits: str of '0'/'1' or np.ndarray
    Returns list of {position, hamming_distance} sorted by position.
    """
    if isinstance(pattern_bits, str):
        pattern = np.array([int(c) for c in pattern_bits], dtype=np.uint8)
    else:
        pattern = np.asarray(pattern_bits, dtype=np.uint8)

    plen = len(pattern)
    matches = []
    for start in range(0, len(bits) - plen + 1):
        window = bits[start:start + plen]
        dist = int(np.sum(window != pattern))
        if dist <= max_hamming:
            matches.append({"position": start, "hamming_distance": dist})
    return matches


def segment_header_payload(bits, sync_positions, pattern_len, header_len):
    """Given sync-word hit positions, carve out header/payload segments."""
    segments = []
    for m in sync_positions:
        start = m["position"]
        header_start = start + pattern_len
        header = bits[header_start:header_start + header_len]
        payload_start = header_start + header_len
        segments.append({
            "sync_position": start,
            "header": header,
            "payload_start": payload_start,
        })
    return segments
