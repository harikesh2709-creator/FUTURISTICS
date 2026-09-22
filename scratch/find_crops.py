from PIL import Image
import os

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
test_dir = r'c:\vs studio\ntro-signal-analyzer\scratch\crops_test'

# Let's crop candidate panels from screen_constellation.png:
# In screen_constellation.png, where is the constellation canvas?
# In typical layout:
# Top header is y=0..70.
# Left panel might be y=80..950, x=0..600.
# Main visualization canvas might be x=400..1500, y=100..700 or similar.
im_c = Image.open(os.path.join(assets_dir, 'screen_constellation.png'))
# Let's save a few horizontal slices and vertical slices to pinpoint
crops = {
    'c_center': (400, 100, 1500, 750),
    'c_left': (50, 100, 650, 750),
    'c_right': (1200, 100, 1850, 750),
    'c_full_body': (40, 80, 1880, 920),
}
for k, box in crops.items():
    im_c.crop(box).save(os.path.join(test_dir, f"{k}.png"))

im_n = Image.open(os.path.join(assets_dir, 'screen_neural_lab.png'))
crops_n = {
    'n_top_panel': (40, 100, 1880, 500),
    'n_mid_panel': (40, 450, 1880, 920),
    'n_center': (350, 120, 1550, 750),
}
for k, box in crops_n.items():
    im_n.crop(box).save(os.path.join(test_dir, f"{k}.png"))

print("Saved test crops")
