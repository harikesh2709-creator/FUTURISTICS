import os
import time
import win32com.client

ppt_path = r"c:\vs studio\ntro-signal-analyzer\SPECTRA_SIH_2026_Strict_Template_Presentation.pptx"
pdf_path = r"c:\vs studio\ntro-signal-analyzer\SPECTRA_SIH_2026_Strict_Template_Presentation.pdf"
out_dir = r"c:\vs studio\ntro-signal-analyzer\exported_strict_template_slides"
os.makedirs(out_dir, exist_ok=True)

try:
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1
    pres = powerpoint.Presentations.Open(os.path.abspath(ppt_path), WithWindow=False)
    time.sleep(1)

    # Export PDF (32 is ppSaveAsPDF)
    pres.SaveAs(os.path.abspath(pdf_path), 32)
    print(f"Exported PDF: {pdf_path}")

    # Export slides as PNG
    for idx, slide in enumerate(pres.Slides):
        png_path = os.path.join(out_dir, f"slide_{idx+1}.png")
        slide.Export(png_path, "PNG", 1920, 1080)
        print(f"Exported Slide {idx+1}: {png_path}")

    pres.Close()
    powerpoint.Quit()
    print("Export completed successfully.")
except Exception as e:
    print(f"Error during export: {e}")
