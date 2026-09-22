from PIL import Image
import numpy as np

sc_neural = r'c:\vs studio\ntro-signal-analyzer\presentation_assets\screen_neural_lab.png'
im = Image.open(sc_neural)
arr = np.array(im)

print("Neural lab x around 200..320 along y=200:")
for x in range(200, 320, 10):
    print(f"x={x}: {arr[200, x]}")
