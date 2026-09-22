from PIL import Image
import os

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
files = [
    'screen_constellation.png',
    'screen_neural_lab.png',
    'screen_risk_console.png',
    'screen_interleaver_solver.png',
    'screen_ground_truth.png',
    'screen_mission_radar.png'
]

for f in files:
    p = os.path.join(assets_dir, f)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"File: {f}, Size: {im.size}")
