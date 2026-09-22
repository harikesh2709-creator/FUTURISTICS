"""
Export draw.io diagram to a high-definition PNG.
This script utilizes the official draw.io rendering engine to guarantee zero degradation
and pixel-perfect conversion without manually interacting with the draw.io desktop app.
"""
import os
import asyncio
from utils.drawio_engine import render_diagram

async def export_drawio():
    drawio_file = r"c:\vs studio\ntro-signal-analyzer\spectra_architecture.drawio"
    out_slide = r"c:\vs studio\ntro-signal-analyzer\presentation_assets\system_architecture_hd.png"
    
    print(f"Initializing Native Draw.io Rendering Engine for {drawio_file}...")
    
    # Render using 6x scale factor (approx 6K resolution) to completely eliminate 
    # any raster degradation when scaled in PowerPoint.
    await render_diagram(
        xml_path=drawio_file,
        out_path=out_slide,
        scale=6
    )
    
    if os.path.exists(out_slide):
        print(f"Successfully generated High-Definition architecture diagrams.")

if __name__ == "__main__":
    asyncio.run(export_drawio())
