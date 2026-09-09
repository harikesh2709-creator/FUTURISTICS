import os
import fitz

src_pdf = r"c:\vs studio\freight-forecast\SIH2026_FreightForecast_Pro_Storm.pdf"
artifact_dir = r"C:\Users\Harik\.gemini\antigravity-ide\brain\218e3fa8-15eb-40a0-9f59-04745317229e"

doc = fitz.open(src_pdf)
print(f"Total pages in PDF: {len(doc)}")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_img = os.path.join(artifact_dir, f"storm_style_slide_{i+1}.png")
    pix.save(out_img)
    print(f"Saved {out_img}")
