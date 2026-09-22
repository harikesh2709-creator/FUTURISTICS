from PIL import Image, ImageEnhance
import os

brain_dir = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb'
assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
sc_hex = os.path.join(brain_dir, 'hex_dump_tab_view_1789130395630.png')

im = Image.open(sc_hex)
# Crop x: 215..1885, y: 85..760
# This includes:
# - Full Turbo Spectrogram / Waterfall
# - Constellation Density Heatmap
# - 1024-Pt Power Spectral Density
# - Extracted Signal Metrics (500 kHz, 2.21 GHz, 151 kHz OBW, 5.55 dB SNR)
# - Modulation Classifier (BPSK 43%)
# - FEC & Framing Telemetry (NASA K=7 R=1/2, Viterbi 491, Interleaving Block d=8)
crop_s4 = im.crop((215, 85, 1885, 760))
crop_s4 = ImageEnhance.Sharpness(crop_s4).enhance(1.25)
p_out = os.path.join(assets_dir, 'crop_risk_spectral_anomaly.png')
crop_s4.save(p_out, quality=98)
print(f"Saved {p_out} size={crop_s4.size}")
