import os
from PIL import Image, ImageEnhance, ImageFilter

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
brain_dir = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb'

# Source screenshots
sc_const = os.path.join(assets_dir, 'screen_constellation.png')
sc_neural = os.path.join(assets_dir, 'screen_neural_lab.png')
sc_hex = os.path.join(brain_dir, 'hex_dump_tab_view_1789130395630.png')
sc_radar = os.path.join(assets_dir, 'screen_mission_radar.png')

# 1. Slide 3 Left Image: Constellation Scatter & Eye Diagram Crop
# In screen_constellation.png: x=35..950, y=145..710
im_const = Image.open(sc_const)
crop1 = im_const.crop((35, 145, 955, 715))
# sharpen slightly for extreme clarity when placed in PPTX
enhancer = ImageEnhance.Sharpness(crop1)
crop1 = enhancer.enhance(1.2)
p_crop1 = os.path.join(assets_dir, 'crop_constellation_clean.png')
crop1.save(p_crop1, quality=95)
print(f"Saved {p_crop1} ({crop1.size})")

# 2. Slide 3 Right Image: AI Neural Modulation Classifier Crop
# In screen_constellation.png: x=965..1885, y=145..710
crop2 = im_const.crop((965, 145, 1885, 715))
enhancer = ImageEnhance.Sharpness(crop2)
crop2 = enhancer.enhance(1.2)
p_crop2 = os.path.join(assets_dir, 'crop_neural_amc_clean.png')
crop2.save(p_crop2, quality=95)
print(f"Saved {p_crop2} ({crop2.size})")

# 3. Slide 4 Image: Contaminated Spectrum & Tactical Anomaly Console
# In screen_neural_lab.png / screen_mission_radar.png:
# Let's crop the Extracted Neural Parameters & Tactical Synthesis & Threat score (x=850..1880, y=550..945)
# or from hex_dump: Waterfall + PSD + Metrics!
# In hex_dump: x=160..1890, y=80..525 (Waterfall + PSD + Extracted Signal Metrics)
im_hex = Image.open(sc_hex)
crop3 = im_hex.crop((160, 80, 1890, 525))
enhancer = ImageEnhance.Sharpness(crop3)
crop3 = enhancer.enhance(1.2)
p_crop3 = os.path.join(assets_dir, 'crop_risk_spectral_anomaly.png')
crop3.save(p_crop3, quality=95)
print(f"Saved {p_crop3} ({crop3.size})")

# 4. Slide 5 Image: Live Bitstream & GF(2) Interleaver Solver
# In hex_dump: Bitstream Hex Dump + Mission Parameter Decode Log + FEC Telemetry (x=160..1890, y=530..965)
crop4 = im_hex.crop((160, 530, 1890, 965))
enhancer = ImageEnhance.Sharpness(crop4)
crop4 = enhancer.enhance(1.2)
p_crop4 = os.path.join(assets_dir, 'crop_interleaver_hex_clean.png')
crop4.save(p_crop4, quality=95)
print(f"Saved {p_crop4} ({crop4.size})")

# 5. Slide 7 Module 1: Telemetry Ingestion, Waveform & Constellation
# In hex_dump: x=160..1520, y=80..525 (Waterfall + Constellation + PSD)
crop5 = im_hex.crop((160, 80, 1520, 525))
enhancer = ImageEnhance.Sharpness(crop5)
crop5 = enhancer.enhance(1.2)
p_crop5 = os.path.join(assets_dir, 'crop_module1_telemetry.png')
crop5.save(p_crop5, quality=95)
print(f"Saved {p_crop5} ({crop5.size})")

# 6. Slide 7 Module 2: AI Neural Intelligence Lab & Parameters
# In screen_neural_lab.png: x=180..1890, y=95..945
im_neural = Image.open(sc_neural)
crop6 = im_neural.crop((180, 95, 1890, 945))
enhancer = ImageEnhance.Sharpness(crop6)
crop6 = enhancer.enhance(1.2)
p_crop6 = os.path.join(assets_dir, 'crop_module2_neural_lab.png')
crop6.save(p_crop6, quality=95)
print(f"Saved {p_crop6} ({crop6.size})")
