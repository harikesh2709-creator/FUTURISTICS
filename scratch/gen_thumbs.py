from PIL import Image
import os

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
out_dir = r'c:\vs studio\ntro-signal-analyzer\scratch\crops_test'
os.makedirs(out_dir, exist_ok=True)

# Let's see what each screenshot has by slicing quadrants or panels
for name in ['screen_constellation.png', 'screen_neural_lab.png', 'screen_risk_console.png', 'screen_interleaver_solver.png', 'screen_ground_truth.png', 'screen_mission_radar.png']:
    p = os.path.join(assets_dir, name)
    im = Image.open(p)
    # save 400x200 thumb
    thumb = im.resize((480, 242), Image.Resampling.LANCZOS)
    thumb.save(os.path.join(out_dir, f"thumb_{name}"))
print("Thumbnails generated in crops_test")
