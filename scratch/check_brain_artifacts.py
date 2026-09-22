import os
from PIL import Image

brain_dir = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb'

targets = [
    'after_demodulate_1789117037898.png',
    'ai_neural_lab_active_1789465781180.png',
    'ai_neural_lab_panel_1789466393802.png',
    'analyzed_state_overview_1789130298705.png',
    'hex_dump_tab_view_1789130395630.png',
    'constellation_view_1789130332686.png',
    'constellation_tab_scatter_1789109501792.png'
]

for t in targets:
    p = os.path.join(brain_dir, t)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{t}: size={im.size}")
