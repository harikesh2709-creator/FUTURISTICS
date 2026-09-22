"""
Frame Parser — Extracts header and payload from synchronized bitstream.
Supports CRC-16 and CRC-32 verification, and provides hex/ASCII dump.
"""

import numpy as np


# ---------------------------------------------------------------------------
# CRC implementations
# ---------------------------------------------------------------------------
def crc16(data: bytes, poly: int = 0x8005, init: int = 0xFFFF) -> int:
    """CRC-16 (IBM/ANSI) computation."""
    crc = init
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc


def crc32(data: bytes, poly: int = 0x04C11DB7, init: int = 0xFFFFFFFF) -> int:
    """CRC-32 computation."""
    crc = init
    for byte in data:
        crc ^= byte << 24
        for _ in range(8):
            if crc & 0x80000000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFFFFFF
    return crc ^ 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Bits ↔ Bytes conversion
# ---------------------------------------------------------------------------
def bits_to_bytes(bits: np.ndarray) -> bytes:
    """Convert bit array to bytes (MSB first, pad with zeros)."""
    n = len(bits)
    pad = (8 - n % 8) % 8
    if pad:
        bits = np.concatenate([bits, np.zeros(pad, dtype=np.uint8)])
    return bytes(np.packbits(bits))


def bytes_to_hex(data: bytes, group: int = 2) -> str:
    """Convert bytes to hex string with grouping."""
    hex_str = data.hex().upper()
    if group > 0:
        return " ".join(hex_str[i:i + group * 2] for i in range(0, len(hex_str), group * 2))
    return hex_str


def bytes_to_ascii(data: bytes) -> str:
    """Convert bytes to printable ASCII (replace non-printable with '.')."""
    return "".join(chr(b) if 32 <= b < 127 else "." for b in data)


# ---------------------------------------------------------------------------
# Frame Parser
# ---------------------------------------------------------------------------
def parse_frames(
    bits: np.ndarray,
    sync_positions: list,
    frame_length: int = 0,
    sync_length: int = 32,
    header_length: int = 0,
    crc_type: str = "none",
    crc_length: int = 0,
) -> dict:
    """
    Parse synchronized bitstream into frames with header and payload.

    Parameters
    ----------
    bits : full bitstream
    sync_positions : list of bit positions where sync word starts
    frame_length : frame length in bits (0 = auto-detect from spacing)
    sync_length : sync word length in bits
    header_length : additional header bits after sync (before payload)
    crc_type : "crc16", "crc32", or "none"
    crc_length : CRC field length in bits (16 or 32)

    Returns dict:
        frames       : list of frame dicts
        total_frames : number of frames parsed
        valid_crc    : number of frames with valid CRC
    """
    if not sync_positions:
        return {"frames": [], "total_frames": 0, "valid_crc": 0}

    # Auto-detect frame length
    if frame_length <= 0 and len(sync_positions) >= 2:
        spacings = [sync_positions[i + 1] - sync_positions[i]
                    for i in range(len(sync_positions) - 1)]
        frame_length = int(np.median(spacings))

    if frame_length <= sync_length:
        frame_length = 256  # Default fallback

    # Set CRC parameters
    if crc_type == "crc16":
        crc_length = 16
    elif crc_type == "crc32":
        crc_length = 32

    frames = []
    valid_crc_count = 0

    for idx, pos in enumerate(sync_positions):
        frame_end = pos + frame_length
        if frame_end > len(bits):
            break

        frame_bits = bits[pos:frame_end]

        # Split: [sync | header | payload | crc]
        sync_bits = frame_bits[:sync_length]
        remaining = frame_bits[sync_length:]

        header_bits = remaining[:header_length] if header_length > 0 else np.array([], dtype=np.uint8)

        if crc_length > 0:
            payload_bits = remaining[header_length:-crc_length] if crc_length < len(remaining) - header_length else remaining[header_length:]
            crc_bits = remaining[-crc_length:] if crc_length < len(remaining) else np.array([], dtype=np.uint8)
        else:
            payload_bits = remaining[header_length:]
            crc_bits = np.array([], dtype=np.uint8)

        # Convert to bytes
        sync_bytes = bits_to_bytes(sync_bits)
        header_bytes = bits_to_bytes(header_bits) if len(header_bits) > 0 else b""
        payload_bytes = bits_to_bytes(payload_bits) if len(payload_bits) > 0 else b""
        crc_bytes = bits_to_bytes(crc_bits) if len(crc_bits) > 0 else b""

        # CRC verification
        crc_valid = None
        crc_computed = None
        if crc_type == "crc16" and len(payload_bytes) > 0:
            crc_computed = crc16(payload_bytes)
            crc_received = int.from_bytes(crc_bytes[:2], "big") if len(crc_bytes) >= 2 else 0
            crc_valid = crc_computed == crc_received
        elif crc_type == "crc32" and len(payload_bytes) > 0:
            crc_computed = crc32(payload_bytes)
            crc_received = int.from_bytes(crc_bytes[:4], "big") if len(crc_bytes) >= 4 else 0
            crc_valid = crc_computed == crc_received

        if crc_valid:
            valid_crc_count += 1

        # Entropy of payload
        if len(payload_bytes) > 0:
            counts = np.bincount(np.frombuffer(payload_bytes, dtype=np.uint8), minlength=256)
            probs = counts / counts.sum()
            probs = probs[probs > 0]
            entropy = -np.sum(probs * np.log2(probs))
        else:
            entropy = 0.0

        frame = {
            "frame_num": idx,
            "bit_position": int(pos),
            "frame_length_bits": frame_length,
            "sync_hex": sync_bytes.hex().upper(),
            "header_hex": header_bytes.hex().upper() if header_bytes else "",
            "payload_hex": bytes_to_hex(payload_bytes),
            "payload_ascii": bytes_to_ascii(payload_bytes),
            "payload_length_bytes": len(payload_bytes),
            "crc_type": crc_type,
            "crc_valid": crc_valid,
            "crc_hex": crc_bytes.hex().upper() if crc_bytes else "",
            "entropy": round(entropy, 3),
        }
        frames.append(frame)

    return {
        "frames": frames,
        "total_frames": len(frames),
        "valid_crc": valid_crc_count,
        "frame_length_bits": frame_length,
    }


def bitstream_hex_dump(
    bits: np.ndarray,
    offset: int = 0,
    length: int = 512,
    bytes_per_line: int = 16,
) -> dict:
    """
    Generate hex + ASCII dump of a bitstream segment.

    Returns dict:
        lines   : list of formatted hex dump lines
        offset  : start offset in bytes
        length  : number of bytes shown
    """
    bit_slice = bits[offset * 8 : (offset + length) * 8]
    data = bits_to_bytes(bit_slice)

    lines = []
    for i in range(0, len(data), bytes_per_line):
        chunk = data[i : i + bytes_per_line]
        addr = f"{offset + i:08X}"
        hex_part = " ".join(f"{b:02X}" for b in chunk)
        hex_part = hex_part.ljust(bytes_per_line * 3 - 1)
        ascii_part = bytes_to_ascii(chunk)
        lines.append(f"{addr}  {hex_part}  |{ascii_part}|")

    return {
        "lines": lines,
        "offset": offset,
        "length": min(length, len(data)),
    }
