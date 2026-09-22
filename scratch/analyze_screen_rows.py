from PIL import Image
import numpy as np

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'

im_c = Image.open(assets_dir + r'\screen_constellation.png')
# let's analyze row brightness to find top navbar, content area, bottom
arr = np.array(im_c)
row_brightness = arr.mean(axis=(1,2))
print("Constellation image size:", im_c.size)
for y in range(0, 970, 50):
    print(f"y={y}: row brightness = {row_brightness[y]:.1f}")

im_n = Image.open(assets_dir + r'\screen_neural_lab.png')
arr_n = np.array(im_n)
row_b_n = arr_n.mean(axis=(1,2))
print("\nNeural lab image size:", im_n.size)
for y in range(0, 970, 50):
    print(f"y={y}: row brightness = {row_b_n[y]:.1f}")
