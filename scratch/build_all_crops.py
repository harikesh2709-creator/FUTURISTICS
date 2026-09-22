import os
from PIL import Image, ImageEnhance

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
brain_dir = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb'

sc_const = os.path.join(assets_dir, 'screen_constellation.png')
sc_neural = os.path.join(assets_dir, 'screen_neural_lab.png')
sc_hex = os.path.join(brain_dir, 'hex_dump_tab_view_1789130395630.png')

# 1. Slide 3 Left: Constellation
im_c = Image.open(sc_const)
c1 = im_c.crop((35, 145, 955, 715))
c1 = ImageEnhance.Sharpness(c1).enhance(1.25)
c1.save(os.path.join(assets_dir, 'crop_constellation_clean.png'), quality=98)

# 2. Slide 3 Right: Neural AMC (tighter crop to remove empty bottom space)
c2 = im_c.crop((965, 145, 1885, 545))
c2 = ImageEnhance.Sharpness(c2).enhance(1.25)
c2.save(os.path.join(assets_dir, 'crop_neural_amc_clean.png'), quality=98)

# 3. Slide 4 Right: Contaminated Spectrum & Signal Anomaly (x=290..1885, y=85..760)
im_h = Image.open(sc_hex)
c3 = im_h.crop((290, 85, 1885, 760))
c3 = ImageEnhance.Sharpness(c3).enhance(1.25)
c3.save(os.path.join(assets_dir, 'crop_risk_spectral_anomaly.png'), quality=98)

# 4. Slide 5 Right: Bitstream Hex Dump & FEC Solver (x=290..1885, y=535..965)
c4 = im_h.crop((290, 535, 1885, 965))
c4 = ImageEnhance.Sharpness(c4).enhance(1.25)
c4.save(os.path.join(assets_dir, 'crop_interleaver_hex_clean.png'), quality=98)

# 5. Slide 7 Module 1: Spectrum & Waveform (x=290..1540, y=85..520)
c5 = im_h.crop((290, 85, 1540, 520))
c5 = ImageEnhance.Sharpness(c5).enhance(1.25)
c5.save(os.path.join(assets_dir, 'crop_module1_telemetry.png'), quality=98)

# 6. Slide 7 Module 2: Neural AMC & Parameters (x=280..1885, y=95..935)
im_n = Image.open(sc_neural)
c6 = im_n.crop((280, 95, 1885, 935))
c6 = ImageEnhance.Sharpness(c6).enhance(1.25)
c6.save(os.path.join(assets_dir, 'crop_module2_neural_lab.png'), quality=98)

print("Regenerated all crops with x=290 margin. Perfect!")
