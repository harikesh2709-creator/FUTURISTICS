import os
from PIL import Image, ImageEnhance

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
brain_dir = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb'

sc_const = os.path.join(assets_dir, 'screen_constellation.png')
sc_neural = os.path.join(assets_dir, 'screen_neural_lab.png')
sc_hex = os.path.join(brain_dir, 'hex_dump_tab_view_1789130395630.png')

# 1. Slide 3 Left: Constellation
im_const = Image.open(sc_const)
crop1 = im_const.crop((35, 145, 955, 715))
crop1 = ImageEnhance.Sharpness(crop1).enhance(1.25)
crop1.save(os.path.join(assets_dir, 'crop_constellation_clean.png'), quality=98)

# 2. Slide 3 Right: Neural AMC (tighter crop to remove empty bottom)
crop2 = im_const.crop((965, 145, 1885, 545))
crop2 = ImageEnhance.Sharpness(crop2).enhance(1.25)
crop2.save(os.path.join(assets_dir, 'crop_neural_amc_clean.png'), quality=98)

# 3. Slide 4 Right: Contaminated Spectrum & Signal Anomaly
im_hex = Image.open(sc_hex)
crop3 = im_hex.crop((215, 85, 1885, 520))
crop3 = ImageEnhance.Sharpness(crop3).enhance(1.25)
crop3.save(os.path.join(assets_dir, 'crop_risk_spectral_anomaly.png'), quality=98)

# 4. Slide 5 Right: Bitstream Hex Dump & FEC Matrix Solver
crop4 = im_hex.crop((195, 535, 1885, 965))
crop4 = ImageEnhance.Sharpness(crop4).enhance(1.25)
crop4.save(os.path.join(assets_dir, 'crop_interleaver_hex_clean.png'), quality=98)

# 5. Slide 7 Module 1: Spectrum & Waveform
crop5 = im_hex.crop((215, 85, 1540, 520))
crop5 = ImageEnhance.Sharpness(crop5).enhance(1.25)
crop5.save(os.path.join(assets_dir, 'crop_module1_telemetry.png'), quality=98)

# 6. Slide 7 Module 2: Neural AMC & Parameters
im_neural = Image.open(sc_neural)
crop6 = im_neural.crop((235, 95, 1885, 935))
crop6 = ImageEnhance.Sharpness(crop6).enhance(1.25)
crop6.save(os.path.join(assets_dir, 'crop_module2_neural_lab.png'), quality=98)

print("Regenerated all 6 crops with pixel-perfect bounds.")
