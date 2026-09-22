"""
Restore exact original untouched presentations from the unmodified source scripts:
1. generate_sih_ppt_signal_analyzer.py -> SPECTRA_SIH_2026_Presentation_Original.pptx (8 slides)
2. generate_sih_ppt.py -> SPECTRA_SIH_2026_Presentation_Original_9Slide.pptx (9 slides)
"""

import os
import shutil
import importlib.util

def run_script_to_file(script_path, output_filename):
    print(f"Loading {script_path}...")
    # Load module
    spec = importlib.util.spec_from_file_location("orig_module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # In module, Presentation is built and saved in main()
    # We can invoke prs build directly
    from pptx import Presentation
    from pptx.util import Inches

    prs = Presentation()
    prs.slide_width = Inches(module.SLIDE_WIDTH)
    prs.slide_height = Inches(module.SLIDE_HEIGHT)

    # Find build_slide_* functions in order
    slide_funcs = []
    idx = 1
    while True:
        func_name = f"build_slide_{idx}"
        if hasattr(module, func_name):
            slide_funcs.append(getattr(module, func_name))
            idx += 1
        else:
            break

    print(f"Found {len(slide_funcs)} slide builders in {script_path}")
    for i, func in enumerate(slide_funcs, 1):
        print(f"  Building slide {i}...")
        func(prs)

    prs.save(output_filename)
    print(f"Saved {output_filename} ({os.path.getsize(output_filename):,} bytes)")

    # Copy to frontend
    frontend_dest = os.path.join("frontend", output_filename)
    shutil.copy2(output_filename, frontend_dest)
    print(f"Copied to {frontend_dest}")

def main():
    print("=" * 60)
    print("Restoring Previous Original Untouched Presentations...")
    print("=" * 60)

    # 1. 8-Slide Original (from generate_sih_ppt_signal_analyzer.py)
    run_script_to_file("generate_sih_ppt_signal_analyzer.py", "SPECTRA_SIH_2026_Presentation_Original.pptx")
    # Also save as explicit 8-slide alias
    shutil.copy2("SPECTRA_SIH_2026_Presentation_Original.pptx", "SPECTRA_SIH_2026_Presentation_Original_8Slide.pptx")
    shutil.copy2("SPECTRA_SIH_2026_Presentation_Original.pptx", os.path.join("frontend", "SPECTRA_SIH_2026_Presentation_Original_8Slide.pptx"))

    # 2. 9-Slide Original (from generate_sih_ppt.py)
    run_script_to_file("generate_sih_ppt.py", "SPECTRA_SIH_2026_Presentation_Original_9Slide.pptx")

    print("=" * 60)
    print("All original previous presentations successfully restored!")
    print("=" * 60)

if __name__ == "__main__":
    main()
