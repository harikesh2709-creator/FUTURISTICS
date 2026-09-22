from PIL import Image
import numpy as np
import os

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'

# Let's inspect the layout of screen_constellation.png, screen_neural_lab.png, screen_interleaver_solver.png, screen_risk_console.png, screen_ground_truth.png
for name in ['screen_constellation.png', 'screen_neural_lab.png', 'screen_risk_console.png', 'screen_interleaver_solver.png']:
    p = os.path.join(assets_dir, name)
    im = Image.open(p)
    arr = np.array(im)
    # let's see non-black or distinct areas
    print(f"=== {name} ({im.size}) ===")
    print("Mean color:", arr.mean(axis=(0,1)))
