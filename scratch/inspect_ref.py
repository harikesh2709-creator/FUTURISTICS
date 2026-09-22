import fitz
import os

pdf_path = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb\.user_uploaded\media_1789534853550.pdf'
out_dir = r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb\ref_extracted'
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
for pno in range(len(doc)):
    page = doc[pno]
    print(f"=== Page {pno+1} Image Placements ===")
    for img in page.get_images():
        xref = img[0]
        rects = page.get_image_rects(xref)
        base = doc.extract_image(xref)
        w, h = base['width'], base['height']
        for r in rects:
            if r.width > 50 and r.height > 50:
                print(f"  xref={xref} dim={w}x{h} bbox=({r.x0:.1f}, {r.y0:.1f}, {r.x1:.1f}, {r.y1:.1f}) w={r.width:.1f} h={r.height:.1f}")
                # save image
                img_path = os.path.join(out_dir, f"p{pno+1}_xref{xref}_{w}x{h}.{base['ext']}")
                if not os.path.exists(img_path):
                    with open(img_path, 'wb') as f:
                        f.write(base['image'])
