from PIL import Image
import os

brain_dir = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb'
out_dir = r'c:\vs studio\ntro-signal-analyzer\scratch\crops_test'

for name in ['hex_dump_tab_view_1789130395630.png', 'after_demodulate_1789117037898.png']:
    p = os.path.join(brain_dir, name)
    if os.path.exists(p):
        im = Image.open(p)
        thumb = im.resize((480, 242), Image.Resampling.LANCZOS)
        thumb.save(os.path.join(out_dir, f"thumb_{name}"))
print("Done")
