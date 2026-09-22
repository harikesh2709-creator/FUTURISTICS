from PIL import Image
import numpy as np

sc_hex = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb\hex_dump_tab_view_1789130395630.png'
im = Image.open(sc_hex)
arr = np.array(im)

# Let's inspect x around 200..320 for row 350
print("Pixel colors along y=350 from x=200 to x=320:")
for x in range(200, 320, 10):
    print(f"x={x}: {arr[350, x]}")

print("\nPixel colors along y=350 from x=1800 to x=1915:")
for x in range(1800, 1915, 10):
    print(f"x={x}: {arr[350, x]}")
