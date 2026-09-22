"""
Physical RF Sample Generator for Data Ingestion
NTRO Problem Statement 26147: Space Technology Theme

Generates authentic, physically accurate .IQ and .wav sample files adhering to:
1. Friis Transmission Equation (Free Space Path Loss & Link Budget)
2. Johnson-Nyquist Thermal Noise Law (P_N = k_B * T_sys * B * F)
3. Relativistic Doppler Frequency Shift & Drift (f_D = v_r/c * f_c, dot{f}_D = a_r/c * f_c)
4. Rician Multipath Fading (Line-of-Sight + Specular/Diffuse ground reflections)
5. Local Oscillator Wiener Phase Noise (Brownian motion phase drift)
6. Hardware Receiver Front-End I/Q Imbalance
7. CCSDS Space Telemetry Framing (ASM 0x1ACFFC1D, Headers, Telemetry Payload, CRC-16)
8. Forward Error Correction (NASA Standard K=7, R=1/2 Convolutional Coding)
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from signal_io.generator import (
    generate_and_save_physical,
    generate_physical_space_signal,
    save_as_iq,
    save_as_wav,
)


def generate_all_physical_samples():
    output_dir = Path(__file__).parent / "sample_data"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("  NTRO SIGINT WORKSTATION — Physical RF Data Ingestion Generator")
    print("  Generating datasets following strict physical propagation laws...")
    print("=" * 70)

    # -----------------------------------------------------------------------
    # Scenario 1: LEO Satellite Telemetry Pass (QPSK)
    # -----------------------------------------------------------------------
    print("\n[1/3] Generating LEO Satellite Telemetry (QPSK)...")
    print("      Carrier: 437.500 MHz (UHF CubeSat Downlink)")
    print("      Slant Range: 650 km | Orbit: 550 km Sun-Synchronous")
    print("      Physics: Friis FSPL (~141 dB) + Johnson-Nyquist Thermal Noise")
    print("               Doppler Shift (+6.1 kHz) + Doppler Chirp (32 Hz/s)")
    print("               Rician Multipath (K=14 dB) + LO Phase Noise (20 Hz)")
    print("      Protocol: CCSDS ASM (0x1ACFFC1D) + NASA K=7 R=1/2 FEC")

    res_leo = generate_and_save_physical(
        output_dir=str(output_dir),
        filename_prefix="satellite_telemetry_qpsk_leo",
        modulation="qpsk",
        sample_rate=1.0e6,
        symbol_rate=100e3,
        carrier_freq_hz=437.5e6,
        distance_km=650.0,
        tx_power_watts=2.0,
        tx_gain_dbi=2.15,
        rx_gain_dbi=14.5,
        system_temp_k=290.0,
        noise_figure_db=2.5,
        relative_velocity_mps=4200.0,
        radial_accel_mps2=32.0,
        rician_k_db=14.0,
        phase_noise_linewidth_hz=20.0,
        iq_gain_imbalance_db=0.2,
        iq_phase_imbalance_deg=1.2,
        num_frames=24,
        apply_fec=True,
        apply_interleaving=True,
        rrc_alpha=0.35,
        seed=101,
    )
    p1 = res_leo["params"]["physics_parameters"]
    print(f"      -> Created: {res_leo['files']['iq']}")
    print(f"      -> Created: {res_leo['files']['wav']}")
    print(f"      -> Link Budget: FSPL={p1['free_space_path_loss_db']} dB | Rx Power={p1['rx_power_dbm']} dBm | SNR={p1['theoretical_snr_db']} dB")

    # -----------------------------------------------------------------------
    # Scenario 2: Deep Space Probe Downlink (BPSK)
    # -----------------------------------------------------------------------
    print("\n[2/3] Generating Deep Space Probe Downlink (BPSK)...")
    print("      Carrier: 2.215 GHz (S-Band Space Research)")
    print("      Slant Range: 45,000 km (High Earth Orbit / Lunar Transfer)")
    print("      Physics: High FSPL (~192 dB) + Deep Space Cryo Noise Temp (120 K)")
    print("               Doppler Shift (+8.8 kHz) | Clean Line-of-Sight (K=25 dB)")
    print("      Protocol: CCSDS ASM (0x1ACFFC1D) + NASA K=7 R=1/2 FEC")

    res_deep = generate_and_save_physical(
        output_dir=str(output_dir),
        filename_prefix="deep_space_downlink_bpsk",
        modulation="bpsk",
        sample_rate=500e3,
        symbol_rate=50e3,
        carrier_freq_hz=2.215e9,
        distance_km=45000.0,
        tx_power_watts=15.0,
        tx_gain_dbi=18.0,
        rx_gain_dbi=32.0,
        system_temp_k=120.0,
        noise_figure_db=1.8,
        relative_velocity_mps=1200.0,
        radial_accel_mps2=5.0,
        rician_k_db=25.0,
        phase_noise_linewidth_hz=10.0,
        iq_gain_imbalance_db=0.1,
        iq_phase_imbalance_deg=0.5,
        num_frames=20,
        apply_fec=True,
        apply_interleaving=True,
        rrc_alpha=0.35,
        seed=202,
    )
    p2 = res_deep["params"]["physics_parameters"]
    print(f"      -> Created: {res_deep['files']['iq']}")
    print(f"      -> Created: {res_deep['files']['wav']}")
    print(f"      -> Link Budget: FSPL={p2['free_space_path_loss_db']} dB | Rx Power={p2['rx_power_dbm']} dBm | SNR={p2['theoretical_snr_db']} dB")

    # -----------------------------------------------------------------------
    # Scenario 3: Tactical UAV Surveillance Link (16-QAM)
    # -----------------------------------------------------------------------
    print("\n[3/3] Generating Tactical UAV High-Rate Link (16-QAM)...")
    print("      Carrier: 5.800 GHz (C-Band Tactical Data Link)")
    print("      Slant Range: 18 km | Speed: 180 km/h (50 m/s)")
    print("      Physics: Terrestrial Multipath Ground Clutter (Rician K=8 dB)")
    print("               Doppler Shift (+966 Hz) | Severe Phase Noise (65 Hz)")
    print("      Protocol: High Order Modulation with Block Interleaving")

    res_uav = generate_and_save_physical(
        output_dir=str(output_dir),
        filename_prefix="tactical_uav_16qam",
        modulation="16qam",
        sample_rate=1.0e6,
        symbol_rate=125e3,
        carrier_freq_hz=5.8e9,
        distance_km=18.0,
        tx_power_watts=5.0,
        tx_gain_dbi=6.0,
        rx_gain_dbi=16.0,
        system_temp_k=300.0,
        noise_figure_db=3.5,
        relative_velocity_mps=50.0,
        radial_accel_mps2=2.0,
        rician_k_db=8.0,
        phase_noise_linewidth_hz=65.0,
        iq_gain_imbalance_db=0.4,
        iq_phase_imbalance_deg=2.5,
        num_frames=30,
        apply_fec=False,
        apply_interleaving=True,
        rrc_alpha=0.25,
        seed=303,
    )
    p3 = res_uav["params"]["physics_parameters"]
    print(f"      -> Created: {res_uav['files']['iq']}")
    print(f"      -> Created: {res_uav['files']['wav']}")
    print(f"      -> Link Budget: FSPL={p3['free_space_path_loss_db']} dB | Rx Power={p3['rx_power_dbm']} dBm | SNR={p3['theoretical_snr_db']} dB")

    print("\n" + "=" * 70)
    print("  ALL PHYSICAL RF DATASETS SUCCESSFULLY GENERATED & SAVED!")
    print(f"  Directory: {output_dir}")
    print("=" * 70)


if __name__ == "__main__":
    generate_all_physical_samples()
