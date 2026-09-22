from PIL import Image
import os

# Let's inspect the files in crops_test
crops_dir = r'c:\vs studio\ntro-signal-analyzer\scratch\crops_test'
for f in os.listdir(crops_dir):
    p = os.path.join(crops_dir, f)
    im = Image.open(p)
    print(f"{f}: {im.size}")
