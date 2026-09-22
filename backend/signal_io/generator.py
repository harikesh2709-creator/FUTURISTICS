"""
Synthetic RF Signal Generator — Produces test .IQ and .wav files with known
signal parameters for end-to-end verification of the analysis pipeline.

Capabilities:
  - Generate baseband modulated signals: BPSK, QPSK, 8-PSK, 16-QAM,
    64-QAM, 2-FSK, 4-FSK.
  - Apply pulse shaping (Root Raised Cosine).
  - Optionally apply convolutional encoding (K=7 NASA standard).
  - Optionally apply block / convolutional interleaving.
  - Prepend sync words (CCSDS ASM, Barker, custom).
  - Add AWGN at configurable SNR.
  - Save as .iq (complex64) or .wav (stereo I/Q, 16-bit PCM).
"""

import struct
import wave
from pathlib import Path
from typing import Optional, Literal

import numpy as np
from scipy.signal import firwin, lfilter

# ---------------------------------------------------------------------------
# Root Raised Cosine filter design
# ---------------------------------------------------------------------------
def design_rrc(num_taps: int, sps: int, alpha: float) -> np.ndarray:
    """Design a Root Raised Cosine (RRC) FIR filter."""
    T = 1.0  # symbol period (normalized)
    Ts = T / sps
    t = np.arange(-num_taps // 2, num_taps // 2 + 1) * Ts

    h = np.zeros_like(t)
    for i, ti in enumerate(t):
        if abs(ti) < 1e-12:
            h[i] = (1 / T) * (1 + alpha * (4 / np.pi - 1))
        elif abs(abs(ti) - T / (4 * alpha)) < 1e-12 and alpha > 0:
            h[i] = (alpha / (T * np.sqrt(2))) * (
                (1 + 2 / np.pi) * np.sin(np.pi / (4 * alpha))
                + (1 - 2 / np.pi) * np.cos(np.pi / (4 * alpha))
            )
        else:
            num = np.sin(np.pi * ti / T * (1 - alpha)) + \
                  4 * alpha * ti / T * np.cos(np.pi * ti / T * (1 + alpha))
            den = np.pi * ti / T * (1 - (4 * alpha * ti / T) ** 2)
            h[i] = (1 / T) * num / (den + 1e-30)

    h /= np.sqrt(np.sum(h ** 2))
    return h


# ---------------------------------------------------------------------------
# Modulation mappers
# ---------------------------------------------------------------------------
def _gray_qpsk() -> np.ndarray:
    """QPSK Gray-coded constellation (normalized)."""
    return np.array([1+1j, -1+1j, -1-1j, 1-1j]) / np.sqrt(2)


def _gray_8psk() -> np.ndarray:
    """8-PSK Gray-coded constellation."""
    gray_order = [0, 1, 3, 2, 6, 7, 5, 4]
    angles = np.array([2 * np.pi * g / 8 for g in gray_order])
    return np.exp(1j * angles)


def _gray_16qam() -> np.ndarray:
    """16-QAM Gray-coded constellation (normalized)."""
    levels = [-3, -1, 1, 3]
    const = np.array([complex(i, q) for q in levels for i in levels])
    return const / np.sqrt(np.mean(np.abs(const) ** 2))


def _gray_64qam() -> np.ndarray:
    """64-QAM Gray-coded constellation (normalized)."""
    levels = [-7, -5, -3, -1, 1, 3, 5, 7]
    const = np.array([complex(i, q) for q in levels for i in levels])
    return const / np.sqrt(np.mean(np.abs(const) ** 2))


_CONSTELLATION = {
    "bpsk":   np.array([1.0 + 0j, -1.0 + 0j]),
    "qpsk":   _gray_qpsk(),
    "8psk":   _gray_8psk(),
    "16qam":  _gray_16qam(),
    "64qam":  _gray_64qam(),
}

_BITS_PER_SYMBOL = {
    "bpsk": 1, "qpsk": 2, "8psk": 3, "16qam": 4, "64qam": 6,
    "2fsk": 1, "4fsk": 2,
}


# ---------------------------------------------------------------------------
# Convolutional encoder (NASA K=7 R=1/2)
# ---------------------------------------------------------------------------
def conv_encode_k7(bits: np.ndarray) -> np.ndarray:
    """
    Rate-1/2 convolutional encoder, constraint length K=7.
    Generator polynomials: G1 = 171₈ (0x79), G2 = 133₈ (0x5B).
    """
    g1 = 0o171  # 0b1111001
    g2 = 0o133  # 0b1011011
    state = 0
    out = []
    for b in bits:
        state = ((state << 1) | int(b)) & 0x7F  # 7-bit shift register
        # XOR parity for each generator
        c1 = bin(state & g1).count("1") % 2
        c2 = bin(state & g2).count("1") % 2
        out.extend([c1, c2])
    return np.array(out, dtype=np.uint8)


# ---------------------------------------------------------------------------
# Interleaver
# ---------------------------------------------------------------------------
def block_interleave(bits: np.ndarray, rows: int, cols: int) -> np.ndarray:
    """
    Block interleaver: write row-wise, read column-wise.
    Pads with zeros if needed.
    """
    total = rows * cols
    n = len(bits)
    if n < total:
        bits = np.concatenate([bits, np.zeros(total - n, dtype=bits.dtype)])
    else:
        bits = bits[:total]
    matrix = bits.reshape(rows, cols)
    return matrix.T.flatten()


# ---------------------------------------------------------------------------
# Main signal generator
# ---------------------------------------------------------------------------
def generate_test_signal(
    modulation: str = "qpsk",
    num_symbols: int = 2048,
    sample_rate: float = 1.0e6,
    symbol_rate: float = 100e3,
    snr_db: float = 15.0,
    center_freq_offset: float = 0.0,
    rrc_alpha: float = 0.35,
    rrc_taps: int = 101,
    apply_fec: bool = False,
    apply_interleaving: bool = False,
    interleave_rows: int = 16,
    interleave_cols: int = 16,
    sync_word_hex: Optional[str] = None,
    seed: int = 42,
) -> dict:
    """
    Generate a synthetic modulated signal with known parameters.

    Returns dict with:
        samples    : np.ndarray complex64
        bits       : np.ndarray uint8 (original data bits)
        coded_bits : np.ndarray uint8 (after FEC if applied)
        symbols    : np.ndarray complex64 (baseband symbols before pulse shaping)
        params     : dict of all ground-truth parameters
    """
    rng = np.random.default_rng(seed)
    mod_key = modulation.lower().replace("-", "")
    bps = _BITS_PER_SYMBOL.get(mod_key, 2)

    # Generate random data bits
    num_data_bits = num_symbols * bps
    data_bits = rng.integers(0, 2, size=num_data_bits).astype(np.uint8)

    # Optional sync word prepend
    if sync_word_hex:
        sync_bytes = bytes.fromhex(sync_word_hex.replace("0x", ""))
        sync_bits = np.unpackbits(np.frombuffer(sync_bytes, dtype=np.uint8))
        data_bits = np.concatenate([sync_bits, data_bits])

    # Optional FEC encoding
    coded_bits = data_bits.copy()
    if apply_fec:
        coded_bits = conv_encode_k7(data_bits)

    # Optional interleaving
    if apply_interleaving:
        coded_bits = block_interleave(coded_bits, interleave_rows, interleave_cols)

    # Trim to whole symbols
    n_syms = len(coded_bits) // bps
    coded_bits = coded_bits[: n_syms * bps]

    sps = max(2, int(round(sample_rate / symbol_rate)))  # samples per symbol

    # ------ Modulate ------
    if mod_key in ("2fsk", "4fsk"):
        symbols, baseband = _modulate_fsk(
            coded_bits, mod_key, sps, sample_rate, symbol_rate, rng
        )
    else:
        const = _CONSTELLATION[mod_key]
        # Map bits to symbol indices
        bit_groups = coded_bits.reshape(-1, bps)
        indices = np.zeros(len(bit_groups), dtype=int)
        for i, bg in enumerate(bit_groups):
            idx = 0
            for b in bg:
                idx = (idx << 1) | int(b)
            indices[i] = idx % len(const)
        symbols = const[indices]

        # Pulse shaping via RRC
        upsampled = np.zeros(len(symbols) * sps, dtype=np.complex64)
        upsampled[::sps] = symbols
        rrc = design_rrc(rrc_taps, sps, rrc_alpha)
        baseband = np.convolve(upsampled, rrc, mode="same").astype(np.complex64)

    # Apply frequency offset (simulate off-center tuning)
    if abs(center_freq_offset) > 0:
        t = np.arange(len(baseband)) / sample_rate
        baseband = baseband * np.exp(1j * 2 * np.pi * center_freq_offset * t).astype(
            np.complex64
        )

    # Add AWGN
    sig_power = np.mean(np.abs(baseband) ** 2)
    snr_lin = 10 ** (snr_db / 10)
    noise_power = sig_power / snr_lin
    noise = np.sqrt(noise_power / 2) * (
        rng.standard_normal(len(baseband)) + 1j * rng.standard_normal(len(baseband))
    )
    noisy = (baseband + noise).astype(np.complex64)

    params = {
        "modulation": modulation,
        "num_symbols": n_syms,
        "sample_rate": sample_rate,
        "symbol_rate": symbol_rate,
        "samples_per_symbol": sps,
        "snr_db": snr_db,
        "center_freq_offset": center_freq_offset,
        "rrc_alpha": rrc_alpha,
        "fec_applied": apply_fec,
        "fec_type": "conv_k7_r12" if apply_fec else "none",
        "interleaving_applied": apply_interleaving,
        "interleave_rows": interleave_rows if apply_interleaving else 0,
        "interleave_cols": interleave_cols if apply_interleaving else 0,
        "sync_word_hex": sync_word_hex or "",
        "num_data_bits": len(data_bits),
        "num_coded_bits": len(coded_bits),
    }

    return {
        "samples": noisy,
        "bits": data_bits,
        "coded_bits": coded_bits,
        "symbols": symbols,
        "params": params,
    }


def _modulate_fsk(
    bits: np.ndarray,
    mod_key: str,
    sps: int,
    sample_rate: float,
    symbol_rate: float,
    rng: np.random.Generator,
) -> tuple:
    """Generate FSK modulated signal."""
    if mod_key == "2fsk":
        M = 2
        bps = 1
    else:
        M = 4
        bps = 2

    freq_dev = symbol_rate * 0.5  # Deviation
    freqs = np.linspace(-freq_dev * (M - 1) / 2, freq_dev * (M - 1) / 2, M)

    n_syms = len(bits) // bps
    bits = bits[: n_syms * bps]

    # Map bits to frequency indices
    bit_groups = bits.reshape(-1, bps)
    indices = np.zeros(n_syms, dtype=int)
    for i, bg in enumerate(bit_groups):
        idx = 0
        for b in bg:
            idx = (idx << 1) | int(b)
        indices[i] = idx

    # Generate continuous-phase FSK
    phase = np.zeros(n_syms * sps)
    for i, idx in enumerate(indices):
        phase[i * sps : (i + 1) * sps] = freqs[idx]

    t = np.arange(len(phase)) / sample_rate
    cumphase = 2 * np.pi * np.cumsum(phase) / sample_rate
    baseband = np.exp(1j * cumphase).astype(np.complex64)

    symbols = np.exp(1j * np.array([freqs[idx] for idx in indices])).astype(np.complex64)

    return symbols, baseband


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------
def save_as_iq(samples: np.ndarray, filepath: str) -> None:
    """Save complex samples as raw complex64 binary (.iq)."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    samples.astype(np.complex64).tofile(filepath)


def save_as_wav(
    samples: np.ndarray, filepath: str, sample_rate: int = 1000000
) -> None:
    """Save complex samples as stereo WAV (I=left, Q=right), 16-bit PCM."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    I = samples.real
    Q = samples.imag
    # Normalize to int16 range
    peak = max(np.max(np.abs(I)), np.max(np.abs(Q)), 1e-12)
    I_int = (I / peak * 32000).astype(np.int16)
    Q_int = (Q / peak * 32000).astype(np.int16)
    # Interleave L, R
    stereo = np.empty(len(I_int) * 2, dtype=np.int16)
    stereo[0::2] = I_int
    stereo[1::2] = Q_int

    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(int(sample_rate))
        wf.writeframes(stereo.tobytes())


def generate_and_save(
    output_dir: str = "sample_data",
    **kwargs,
) -> dict:
    """Generate a test signal and save as both .iq and .wav files."""
    result = generate_test_signal(**kwargs)
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    mod = kwargs.get("modulation", "qpsk")
    snr = kwargs.get("snr_db", 15.0)
    prefix = f"{mod}_snr{int(snr)}db"

    iq_path = str(outdir / f"{prefix}.iq")
    wav_path = str(outdir / f"{prefix}.wav")
    save_as_iq(result["samples"], iq_path)
    save_as_wav(result["samples"], wav_path, int(result["params"]["sample_rate"]))

    # Save ground truth metadata
    import json
    meta_path = str(outdir / f"{prefix}_meta.json")
    with open(meta_path, "w") as f:
        json.dump(result["params"], f, indent=2)

    result["files"] = {"iq": iq_path, "wav": wav_path, "meta": meta_path}
    return result


# ===========================================================================
# Physical RF Propagation & Real-World Channel Models
# (Friis Path Loss, Johnson-Nyquist Noise, Doppler Dynamics, Rician Multipath,
#  Wiener Phase Noise, Hardware I/Q Imbalance, CCSDS Space Telemetry Framing)
# ===========================================================================

SPEED_OF_LIGHT = 299792458.0   # Speed of light in vacuum (m/s)
BOLTZMANN_K = 1.380649e-23     # Boltzmann constant (J/K)
CCSDS_ASM_32 = bytes.fromhex("1ACFFC1D")  # Standard 32-bit Attached Sync Marker


def crc16_ccitt(data: bytes, poly: int = 0x1021, init: int = 0xFFFF) -> int:
    """Standard CCSDS CRC-16 (CCITT) error detection checksum."""
    crc = init
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def compute_friis_rx_power(
    tx_power_watts: float,
    carrier_freq_hz: float,
    distance_m: float,
    tx_gain_dbi: float = 0.0,
    rx_gain_dbi: float = 0.0,
) -> tuple:
    """
    Calculate received RF power via the Friis transmission equation:
    P_rx = P_tx * G_tx * G_rx * (c / (4 * pi * d * f_c))^2
    """
    wavelength = SPEED_OF_LIGHT / carrier_freq_hz
    fspl_linear = (4.0 * np.pi * max(distance_m, 1.0) / wavelength) ** 2
    fspl_db = float(10.0 * np.log10(fspl_linear))
    g_tx_lin = 10.0 ** (tx_gain_dbi / 10.0)
    g_rx_lin = 10.0 ** (rx_gain_dbi / 10.0)
    rx_power_watts = float((tx_power_watts * g_tx_lin * g_rx_lin) / fspl_linear)
    return rx_power_watts, fspl_db


def compute_johnson_nyquist_noise(
    bandwidth_hz: float,
    system_temp_k: float = 290.0,
    noise_figure_db: float = 2.5,
) -> tuple:
    """
    Calculate thermal noise power from the Johnson-Nyquist physical law:
    P_noise = k_B * T_sys * B * F
    """
    f_lin = 10.0 ** (noise_figure_db / 10.0)
    noise_power_watts = float(BOLTZMANN_K * system_temp_k * bandwidth_hz * f_lin)
    n0_watts_hz = BOLTZMANN_K * system_temp_k * f_lin
    n0_dbm_hz = float(10.0 * np.log10(n0_watts_hz * 1000.0))
    return noise_power_watts, n0_dbm_hz


def apply_doppler_dynamics(
    samples: np.ndarray,
    sample_rate: float,
    carrier_freq_hz: float,
    relative_velocity_mps: float,
    radial_accel_mps2: float = 0.0,
) -> tuple:
    """
    Apply physical Doppler shift and radial acceleration drift:
    f_D(t) = (v_r / c) * f_c + (a_r / c) * f_c * t
    """
    t = np.arange(len(samples)) / sample_rate
    f_d0 = (relative_velocity_mps / SPEED_OF_LIGHT) * carrier_freq_hz
    f_dot = (radial_accel_mps2 / SPEED_OF_LIGHT) * carrier_freq_hz
    phase = 2.0 * np.pi * (f_d0 * t + 0.5 * f_dot * (t ** 2))
    shifted = samples * np.exp(1j * phase).astype(np.complex64)
    info = {
        "doppler_shift_hz": float(round(f_d0, 2)),
        "doppler_drift_hz_s": float(round(f_dot, 3)),
        "relative_velocity_mps": float(relative_velocity_mps),
        "radial_accel_mps2": float(radial_accel_mps2),
    }
    return shifted, info


def apply_rician_multipath(
    samples: np.ndarray,
    sample_rate: float,
    k_factor_db: float = 12.0,
    delays_sec: Optional[list] = None,
    gains_db: Optional[list] = None,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Apply physical Rician fading multipath channel (LOS path + diffuse reflections).
    """
    if rng is None:
        rng = np.random.default_rng(42)
    k_linear = 10.0 ** (k_factor_db / 10.0)
    los_weight = np.sqrt(k_linear / (k_linear + 1.0))
    nlos_weight = np.sqrt(1.0 / (k_linear + 1.0))

    if delays_sec is None:
        delays_sec = [1.2e-7, 3.5e-7]
        gains_db = [-7.0, -13.0]

    out = (los_weight * samples).astype(np.complex64)
    diffuse = np.zeros_like(samples, dtype=np.complex64)
    total_gain = 0.0

    for tau, g_db in zip(delays_sec, gains_db):
        shift = int(round(tau * sample_rate))
        if 0 < shift < len(samples):
            amp = 10.0 ** (g_db / 20.0)
            phase = rng.uniform(0, 2 * np.pi)
            coeff = amp * np.exp(1j * phase)
            delayed = np.zeros_like(samples)
            delayed[shift:] = samples[:-shift]
            diffuse += (coeff * delayed).astype(np.complex64)
            total_gain += amp ** 2

    if total_gain > 0:
        diffuse /= np.sqrt(total_gain)
        out += (nlos_weight * diffuse).astype(np.complex64)

    return out


def apply_phase_noise(
    samples: np.ndarray,
    sample_rate: float,
    linewidth_hz: float = 25.0,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Apply Wiener phase noise (Brownian motion phase drift in crystal LOs).
    """
    if rng is None:
        rng = np.random.default_rng(42)
    dt = 1.0 / sample_rate
    sigma = np.sqrt(2.0 * np.pi * linewidth_hz * dt)
    d_phi = rng.normal(0.0, sigma, size=len(samples))
    phi = np.cumsum(d_phi)
    return (samples * np.exp(1j * phi)).astype(np.complex64)


def apply_iq_imbalance(
    samples: np.ndarray,
    gain_imbalance_db: float = 0.2,
    phase_imbalance_deg: float = 1.2,
) -> np.ndarray:
    """
    Apply receiver front-end analog I/Q quadrature mixer imbalance.
    """
    g = 10.0 ** (gain_imbalance_db / 20.0)
    phi = np.radians(phase_imbalance_deg)
    I = samples.real * g
    Q = samples.imag * np.cos(phi) - I * np.sin(phi)
    return (I + 1j * Q).astype(np.complex64)


def build_ccsds_telemetry_packet(
    seq_counter: int,
    apid: int = 0x042,
    timestamp_sec: float = 1726050000.0,
) -> bytes:
    """
    Build an authentic CCSDS Telemetry Space Packet with Attached Sync Marker (ASM 0x1ACFFC1D).
    Payload contains simulated satellite flight telemetry:
      - 32-bit ASM (0x1ACFFC1D)
      - 6-byte CCSDS Header
      - Secondary Header (Mission Elapsed Time)
      - Bus telemetry: Battery Voltage (V), Solar Current (A), Bus Temp (degC), Wheel RPM, GPS
      - CRC-16 CCITT
    """
    packet_id = (0 << 13) | (0 << 12) | (1 << 11) | (apid & 0x07FF)
    packet_seq = (3 << 14) | (seq_counter & 0x3FFF)

    t_int = int(timestamp_sec) + seq_counter
    v_bat = float(8.2 + 0.1 * np.sin(seq_counter * 0.1))
    i_sol = float(1.45 + 0.05 * np.cos(seq_counter * 0.1))
    temp_c = float(21.5 + 0.3 * np.sin(seq_counter * 0.05))
    wheel_rpm = int(3200 + 50 * np.sin(seq_counter * 0.2)) & 0xFFFF
    gyro_z = int(120 * np.cos(seq_counter * 0.1)) & 0xFFFF
    gps_lat = 28.6139  # ISRO / NTRO coordinates (New Delhi)
    gps_lon = 77.2090
    gps_alt = 550.0e3  # 550 km LEO altitude

    payload = struct.pack(
        ">IfffHHfff",
        t_int, v_bat, i_sol, temp_c, wheel_rpm, gyro_z,
        gps_lat, gps_lon, gps_alt,
    )

    data_length = len(payload) + 2 - 1
    header = struct.pack(">HHH", packet_id, packet_seq, data_length)
    packet_pre_crc = header + payload
    crc = crc16_ccitt(packet_pre_crc)
    full_packet = CCSDS_ASM_32 + packet_pre_crc + struct.pack(">H", crc)
    return full_packet


def generate_physical_space_signal(
    modulation: str = "qpsk",
    sample_rate: float = 1.0e6,
    symbol_rate: float = 100e3,
    carrier_freq_hz: float = 437.5e6,    # UHF CubeSat Downlink
    distance_km: float = 600.0,          # 600 km LEO
    tx_power_watts: float = 2.0,         # 2 Watts transmitter
    tx_gain_dbi: float = 2.15,           # Dipole antenna
    rx_gain_dbi: float = 14.5,           # 14.5 dBi ground station Yagi
    system_temp_k: float = 290.0,        # Standard thermal noise temp
    noise_figure_db: float = 2.5,        # 2.5 dB LNA Noise Figure
    relative_velocity_mps: float = 4200.0,# 4.2 km/s radial velocity
    radial_accel_mps2: float = 30.0,     # Doppler rate
    rician_k_db: float = 13.0,           # Rician multipath K-factor
    phase_noise_linewidth_hz: float = 25.0, # LO phase noise
    iq_gain_imbalance_db: float = 0.2,   # 0.2 dB front-end gain imbalance
    iq_phase_imbalance_deg: float = 1.2, # 1.2 deg mixer phase imbalance
    num_frames: int = 24,                # Number of CCSDS frames
    apply_fec: bool = True,              # NASA K=7 R=1/2 convolutional FEC
    apply_interleaving: bool = True,     # Block interleaving
    interleave_rows: int = 16,
    interleave_cols: int = 16,
    rrc_alpha: float = 0.35,
    seed: int = 101,
) -> dict:
    """
    Generate an authentic space signal strictly governed by physical laws:
    1. Continuous stream of CCSDS telemetry packets with 32-bit ASM (0x1ACFFC1D).
    2. Convolutional forward error correction (NASA K=7, R=1/2) and interleaving.
    3. Gray-coded constellation mapping and Root Raised Cosine pulse shaping.
    4. Friis Transmission Equation path loss.
    5. Doppler frequency shift and acceleration chirp.
    6. Rician multipath channel fading.
    7. Local oscillator Wiener phase noise.
    8. Receiver front-end I/Q quadrature imbalance.
    9. Johnson-Nyquist thermal noise floor.
    """
    rng = np.random.default_rng(seed)
    mod_key = modulation.lower().replace("-", "").replace("_", "")
    bps = _BITS_PER_SYMBOL.get(mod_key, 2)

    # 1. Assemble CCSDS Telemetry Bitstream
    all_packets = bytearray()
    for seq in range(num_frames):
        packet = build_ccsds_telemetry_packet(seq_counter=seq)
        all_packets.extend(packet)

    data_bytes = bytes(all_packets)
    data_bits = np.unpackbits(np.frombuffer(data_bytes, dtype=np.uint8))

    # 2. Forward Error Correction
    coded_bits = data_bits.copy()
    if apply_fec:
        coded_bits = conv_encode_k7(data_bits)

    # 3. Interleaving
    if apply_interleaving:
        blk_size = interleave_rows * interleave_cols
        n_blocks = max(1, len(coded_bits) // blk_size)
        total_len = n_blocks * blk_size
        if len(coded_bits) < total_len:
            coded_bits = np.pad(coded_bits, (0, total_len - len(coded_bits)))
        else:
            coded_bits = coded_bits[:total_len]
        interleaved_blocks = []
        for b in range(n_blocks):
            blk = coded_bits[b * blk_size : (b + 1) * blk_size]
            interleaved_blocks.append(block_interleave(blk, interleave_rows, interleave_cols))
        coded_bits = np.concatenate(interleaved_blocks)

    # Align with symbol boundary
    n_syms = len(coded_bits) // bps
    coded_bits = coded_bits[: n_syms * bps]

    sps = max(2, int(round(sample_rate / symbol_rate)))

    # 4. Modulate & Pulse Shape
    const = _CONSTELLATION.get(mod_key, _gray_qpsk())
    bit_groups = coded_bits.reshape(-1, bps)
    indices = np.zeros(len(bit_groups), dtype=int)
    for i, bg in enumerate(bit_groups):
        idx = 0
        for b in bg:
            idx = (idx << 1) | int(b)
        indices[i] = idx % len(const)
    symbols = const[indices]

    upsampled = np.zeros(len(symbols) * sps, dtype=np.complex64)
    upsampled[::sps] = symbols
    rrc = design_rrc(101, sps, rrc_alpha)
    tx_baseband = np.convolve(upsampled, rrc, mode="same").astype(np.complex64)

    # 5. Physical Link Budget (Friis Law)
    dist_m = distance_km * 1000.0
    rx_power_watts, fspl_db = compute_friis_rx_power(
        tx_power_watts=tx_power_watts,
        carrier_freq_hz=carrier_freq_hz,
        distance_m=dist_m,
        tx_gain_dbi=tx_gain_dbi,
        rx_gain_dbi=rx_gain_dbi,
    )
    rx_power_dbm = float(10.0 * np.log10(rx_power_watts * 1000.0))

    # 6. Physical Thermal Noise (Johnson-Nyquist Law)
    noise_bw_hz = sample_rate
    noise_power_watts, n0_dbm_hz = compute_johnson_nyquist_noise(
        bandwidth_hz=noise_bw_hz,
        system_temp_k=system_temp_k,
        noise_figure_db=noise_figure_db,
    )
    noise_power_dbm = float(10.0 * np.log10(noise_power_watts * 1000.0))
    theoretical_snr_db = float(rx_power_dbm - noise_power_dbm)

    # Normalize TX baseband to unit power, then scale to received physical power
    p_norm = np.mean(np.abs(tx_baseband) ** 2)
    sig = (tx_baseband / np.sqrt(p_norm + 1e-30) * np.sqrt(rx_power_watts)).astype(np.complex64)

    # 7. Apply Doppler Dynamics (Relativistic Wave Mechanics)
    sig, doppler_info = apply_doppler_dynamics(
        sig, sample_rate, carrier_freq_hz, relative_velocity_mps, radial_accel_mps2
    )

    # 8. Apply Rician Multipath Propagation
    sig = apply_rician_multipath(
        sig, sample_rate, k_factor_db=rician_k_db, rng=rng
    )

    # 9. Apply Oscillator Phase Noise (Wiener Process)
    sig = apply_phase_noise(
        sig, sample_rate, linewidth_hz=phase_noise_linewidth_hz, rng=rng
    )

    # 10. Apply Hardware I/Q Imbalance
    sig = apply_iq_imbalance(
        sig, gain_imbalance_db=iq_gain_imbalance_db, phase_imbalance_deg=iq_phase_imbalance_deg
    )

    # 11. Add Physical Johnson-Nyquist Thermal Noise
    noise = (np.sqrt(noise_power_watts / 2.0) * (
        rng.standard_normal(len(sig)) + 1j * rng.standard_normal(len(sig))
    )).astype(np.complex64)
    rx_signal = (sig + noise).astype(np.complex64)

    # Normalize output amplitude for standard DAC / ADC dynamic range
    max_amp = float(np.max(np.abs(rx_signal)) + 1e-12)
    rx_signal_norm = (rx_signal / max_amp * 0.9).astype(np.complex64)

    params = {
        "signal_type": "physical_space_telemetry",
        "standard": "CCSDS Telemetry / NASA Deep Space Link",
        "modulation": modulation.upper(),
        "carrier_freq_hz": carrier_freq_hz,
        "sample_rate": sample_rate,
        "symbol_rate": symbol_rate,
        "samples_per_symbol": sps,
        "num_symbols": n_syms,
        "duration_sec": float(len(rx_signal_norm) / sample_rate),
        "num_samples": len(rx_signal_norm),
        "num_ccsds_frames": num_frames,
        "frame_sync_word": "0x1ACFFC1D (CCSDS ASM)",
        "fec_applied": apply_fec,
        "fec_scheme": "NASA Standard K=7, R=1/2 (G1=171o, G2=133o)" if apply_fec else "None",
        "interleaving_applied": apply_interleaving,
        "interleaver": f"Block ({interleave_rows}x{interleave_cols})" if apply_interleaving else "None",
        "physics_parameters": {
            "slant_range_km": float(distance_km),
            "tx_power_watts": float(tx_power_watts),
            "tx_power_dbm": round(float(10.0 * np.log10(tx_power_watts * 1000.0)), 2),
            "free_space_path_loss_db": round(fspl_db, 2),
            "rx_power_dbm": round(rx_power_dbm, 2),
            "noise_density_dbm_per_hz": round(n0_dbm_hz, 2),
            "system_noise_temp_kelvin": float(system_temp_k),
            "receiver_noise_figure_db": float(noise_figure_db),
            "total_thermal_noise_power_dbm": round(noise_power_dbm, 2),
            "theoretical_snr_db": round(theoretical_snr_db, 2),
            "doppler_shift_hz": doppler_info["doppler_shift_hz"],
            "doppler_drift_hz_per_sec": doppler_info["doppler_drift_hz_s"],
            "rician_k_factor_db": float(rician_k_db),
            "lo_phase_noise_linewidth_hz": float(phase_noise_linewidth_hz),
            "iq_gain_imbalance_db": float(iq_gain_imbalance_db),
            "iq_phase_imbalance_deg": float(iq_phase_imbalance_deg),
        },
    }

    return {
        "samples": rx_signal_norm,
        "bits": data_bits,
        "coded_bits": coded_bits,
        "symbols": symbols,
        "params": params,
        "raw_bytes": data_bytes,
    }


def generate_and_save_physical(
    output_dir: str = "sample_data",
    filename_prefix: str = "satellite_telemetry_qpsk_leo",
    **kwargs,
) -> dict:
    """Generate a physical space signal and save as .iq, .wav, and .json metadata."""
    result = generate_physical_space_signal(**kwargs)
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    iq_path = str(outdir / f"{filename_prefix}.iq")
    wav_path = str(outdir / f"{filename_prefix}.wav")
    meta_path = str(outdir / f"{filename_prefix}_meta.json")

    save_as_iq(result["samples"], iq_path)
    save_as_wav(result["samples"], wav_path, int(result["params"]["sample_rate"]))

    import json
    with open(meta_path, "w") as f:
        json.dump(result["params"], f, indent=2)

    result["files"] = {"iq": iq_path, "wav": wav_path, "meta": meta_path}
    return result

