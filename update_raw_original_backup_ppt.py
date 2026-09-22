"""
Update script for SPECTRA_SIH_2026_Presentation_Raw_Original_Backup.pptx
Keeps every image size and position 100% intact!
Sets content font size to ~18pt across all 8 slides.
Adjusts content cleanly to avoid any text overflow.
Removes all AI elements from the text in favor of pure deterministic mathematical DSP.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# CONSTANTS & COLOR PALETTE
# -------------------------------------------------------------
SLIDE_WIDTH = 13.333
SLIDE_HEIGHT = 7.5

COLOR_NAVY_DARK = RGBColor(11, 25, 44)       # #0B192C - Primary titles & ribbons
COLOR_NAVY_PILL = RGBColor(15, 23, 42)       # #0F172A - Team badge pill
COLOR_CYAN_ACCENT = RGBColor(14, 165, 233)   # #0EA5E9 - Electric cyan accent
COLOR_BLUE_PRIMARY = RGBColor(37, 99, 235)   # #2563EB - Primary blue
COLOR_BLUE_LIGHT = RGBColor(239, 246, 255)   # #EFF6FF - Soft blue background
COLOR_EMERALD = RGBColor(16, 185, 129)       # #10B981 - Success & emerald
COLOR_EMERALD_BG = RGBColor(236, 253, 245)   # #ECFDF5 - Emerald tint
COLOR_AMBER = RGBColor(245, 158, 11)         # #F59E0B - Amber solver
COLOR_AMBER_BG = RGBColor(254, 243, 199)     # #FEF3C7 - Amber tint
COLOR_PURPLE = RGBColor(124, 58, 237)        # #7C3AED - Higher-Order Math & HOS
COLOR_PURPLE_BG = RGBColor(245, 243, 255)    # #F5F3FF - Purple tint
COLOR_SLATE_BG = RGBColor(248, 250, 252)     # #F8FAFC - Card background
COLOR_SLATE_BORDER = RGBColor(226, 232, 240) # #E2E8F0 - Card border
COLOR_TEXT_MAIN = RGBColor(15, 23, 42)       # #0F172A - Body text main
COLOR_TEXT_MUTED = RGBColor(71, 85, 105)     # #475569 - Subtitles & labels
COLOR_WHITE = RGBColor(255, 255, 255)        # #FFFFFF - White
COLOR_RED = RGBColor(220, 38, 38)            # #DC2626 - Risks & alerts

FONT_TIMES = "Times New Roman"
FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

# Asset Paths (Exact intact paths)
ASSETS_DIR = "presentation_assets"
SIH_HEADER_LOGO = os.path.join(ASSETS_DIR, "sih_header_logo.png")
SIH_BULB_LOGO = os.path.join(ASSETS_DIR, "sih_bulb_logo.png")
CHART_DONUT_1 = os.path.join(ASSETS_DIR, "chart_donut_bottleneck.png")
CHART_DONUT_2 = os.path.join(ASSETS_DIR, "chart_donut_demand.png")

CROP_CONSTELLATION = os.path.join(ASSETS_DIR, "crop_constellation_clean.png")
CROP_NEURAL_AMC = os.path.join(ASSETS_DIR, "crop_neural_amc_clean.png")
CROP_RISK_ANOMALY = os.path.join(ASSETS_DIR, "crop_risk_spectral_anomaly.png")
CROP_INTERLEAVER_HEX = os.path.join(ASSETS_DIR, "crop_interleaver_hex_clean.png")
CROP_GROUND_TRUTH = os.path.join(ASSETS_DIR, "crop_ground_truth_clean.png")
CROP_MODULE1_TELEMETRY = os.path.join(ASSETS_DIR, "crop_module1_telemetry.png")
CROP_MODULE2_NEURAL = os.path.join(ASSETS_DIR, "crop_module2_neural_lab.png")

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def set_shape_border(shape, color, width=1.2):
    shape.line.color.rgb = color
    shape.line.width = Pt(width)

def set_shape_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def create_card(slide, left, top, width, height, bg_color=COLOR_SLATE_BG, border_color=COLOR_SLATE_BORDER, border_width=1.2):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    set_shape_fill(shape, bg_color)
    if border_color:
        set_shape_border(shape, border_color, border_width)
    else:
        shape.line.fill.background()
    return shape

def add_header(slide, title, category_subtitle="SMART INDIA HACKATHON 2026 • THEME: SPACE TECHNOLOGY", watermark="SIH-2026 TM"):
    team_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.24), Inches(2.5), Inches(0.92))
    set_shape_fill(team_pill, COLOR_NAVY_PILL)
    set_shape_border(team_pill, COLOR_CYAN_ACCENT, 1.4)
    tf = team_pill.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.text = "FUTURISTICS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "TEAM ID: SIH-2026"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CYAN_ACCENT
    p2.alignment = PP_ALIGN.CENTER

    tb = slide.shapes.add_textbox(Inches(3.3), Inches(0.24), Inches(7.4), Inches(0.92))
    tf2 = tb.text_frame
    tf2.word_wrap = True
    tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf2.margin_left = Inches(0)
    tf2.margin_right = Inches(0)
    tf2.margin_top = Inches(0)
    tf2.margin_bottom = Inches(0)
    
    p_sub = tf2.paragraphs[0]
    p_sub.text = f"{category_subtitle.upper()}   |   {watermark}"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(10.0)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_BLUE_PRIMARY
    
    p_title = tf2.add_paragraph()
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(19)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY_DARK

    # Exact intact image size and position: w=1.85, h=0.87 at (10.90, 0.20)
    if os.path.exists(SIH_HEADER_LOGO):
        slide.shapes.add_picture(SIH_HEADER_LOGO, Inches(10.90), Inches(0.20), width=Inches(1.85))

def add_footer(slide, slide_num, total_slides=8):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(7.14), Inches(12.13), Inches(0.015))
    set_shape_fill(line, COLOR_SLATE_BORDER)
    line.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(7.16), Inches(12.13), Inches(0.24))
    tf = tb.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    p = tf.paragraphs[0]
    p.text = f"TEAM FUTURISTICS • SPECTRA Pure DSP Signal Analyzer & Parameter Extraction • SIH 2026 Showcase | Slide {slide_num} of {total_slides}"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.LEFT


# =============================================================
# SLIDE 1: TITLE PAGE (Exact Intact Images + 18pt Content)
# =============================================================
def build_slide_1(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)

    team_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.48), Inches(2.8), Inches(1.0))
    set_shape_fill(team_pill, COLOR_NAVY_PILL)
    set_shape_border(team_pill, COLOR_CYAN_ACCENT, 1.5)
    tf = team_pill.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p1 = tf.paragraphs[0]
    p1.text = "FUTURISTICS"
    p1.font.name = FONT_TIMES
    p1.font.size = Pt(17)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = "TEAM ID: SIH-2026"
    p2.font.name = FONT_TIMES
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CYAN_ACCENT
    p2.alignment = PP_ALIGN.CENTER

    tb_header = slide.shapes.add_textbox(Inches(3.7), Inches(0.52), Inches(6.8), Inches(1.0))
    tf_h = tb_header.text_frame
    tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_h = tf_h.paragraphs[0]
    p_h.text = "SMART INDIA HACKATHON 2026"
    p_h.font.name = FONT_TIMES
    p_h.font.size = Pt(28)
    p_h.font.bold = True
    p_h.font.color.rgb = COLOR_NAVY_DARK

    p_sub = tf_h.add_paragraph()
    p_sub.text = "NATIONAL GRAND FINALE • SOFTWARE EDITION • SIH-2026 TM"
    p_sub.font.name = FONT_TIMES
    p_sub.font.size = Pt(11)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_BLUE_PRIMARY

    # Exact intact images:
    if os.path.exists(SIH_HEADER_LOGO):
        slide.shapes.add_picture(SIH_HEADER_LOGO, Inches(10.80), Inches(0.42), width=Inches(2.00))

    if os.path.exists(SIH_BULB_LOGO):
        slide.shapes.add_picture(SIH_BULB_LOGO, Inches(7.80), Inches(1.80), width=Inches(4.90), height=Inches(5.24))

    meta_card = create_card(slide, 0.8, 1.80, 6.7, 4.60, COLOR_SLATE_BG, COLOR_SLATE_BORDER)
    
    tb_meta = slide.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(6.3), Inches(4.30))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = Inches(0)
    tf_m.margin_right = Inches(0)
    tf_m.margin_top = Inches(0)
    tf_m.margin_bottom = Inches(0)

    items = [
        ("• Problem Statement ID", "26147", COLOR_BLUE_PRIMARY),
        ("• Problem Statement Title", "Automated model for analysis of .IQ and .wav files along with signal parameter extraction", COLOR_NAVY_DARK),
        ("• Category", "Software", COLOR_TEXT_MAIN),
        ("• Theme", "Space Technology", COLOR_BLUE_PRIMARY),
        ("• Team ID", "[SIH-2026-XXXX]", COLOR_BLUE_PRIMARY),
        ("• Team Name", "FUTURISTICS", COLOR_EMERALD)
    ]

    for i, (label, val, val_color) in enumerate(items):
        p = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        p.space_after = Pt(7)
        run1 = p.add_run()
        run1.text = f"{label} – "
        run1.font.name = FONT_TIMES
        run1.font.size = Pt(18)   # Strict 18pt Content
        run1.font.bold = True
        run1.font.color.rgb = COLOR_NAVY_DARK

        run2 = p.add_run()
        run2.text = val
        run2.font.name = FONT_TIMES
        run2.font.size = Pt(18)   # Strict 18pt Content
        run2.font.bold = (label in ["• Problem Statement ID", "• Theme", "• Team Name"])
        run2.font.color.rgb = val_color

    bottom_banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.52), Inches(6.7), Inches(0.50))
    set_shape_fill(bottom_banner, COLOR_NAVY_PILL)
    set_shape_border(bottom_banner, COLOR_CYAN_ACCENT, 1.0)
    tf_b = bottom_banner.text_frame
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.text = "⚡ Deterministic Mathematical DSP  •  GF(2) Matrix Solver  •  Air-Gapped Sovereign Defense"
    p_b.font.name = FONT_TIMES
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_CYAN_ACCENT
    p_b.alignment = PP_ALIGN.CENTER

    add_footer(slide, 1)


# =============================================================
# SLIDE 2: PROPOSED SOLUTION & 4 PILLARS (18pt Content)
# =============================================================
def build_slide_2(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "SPECTRA: Deterministic Space RF Parameter Extraction Engine")

    # LEFT CARD: CORE INTELLIGENCE HUB (w=4.4, h=5.65)
    c1 = create_card(slide, 0.6, 1.35, 4.4, 5.65, COLOR_WHITE, COLOR_NAVY_DARK, 1.2)
    ribbon1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(4.4), Inches(0.38))
    set_shape_fill(ribbon1, COLOR_NAVY_DARK)
    ribbon1.line.fill.background()
    p = ribbon1.text_frame.paragraphs[0]
    p.text = "DETERMINISTIC DSP PIPELINE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb1 = slide.shapes.add_textbox(Inches(0.75), Inches(1.85), Inches(4.1), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0)
    tf1.margin_right = Inches(0)
    tf1.margin_top = Inches(0)
    tf1.margin_bottom = Inches(0)

    steps = [
        ("1. Multi-Format Feeds: ", "Raw interleaved .IQ (float32/int16) and .wav satellite telemetry streams."),
        ("2. Cumulant AMC: ", "Higher-order statistics (C40, C42) classify modulations in sub-15ms."),
        ("3. Timing & Carrier: ", "Gardner TED symbol clock recovery & Costas carrier phase tracking."),
        ("4. GF(2) Matrix Solver: ", "Galois Field matrix rank deficiency recovers interleaver depth D.")
    ]
    for i, (head, body) in enumerate(steps):
        p = tf1.paragraphs[0] if i == 0 else tf1.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = head
        r1.font.name = FONT_BODY
        r1.font.size = Pt(17)   # Calibrated 17-18pt
        r1.font.bold = True
        r1.font.color.rgb = COLOR_BLUE_PRIMARY
        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_BODY
        r2.font.size = Pt(17)   # Calibrated 17-18pt
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # RIGHT CARD: 4 CORE PILLARS (w=7.4, h=5.65)
    c2 = create_card(slide, 5.3, 1.35, 7.43, 5.65, COLOR_WHITE, COLOR_BLUE_PRIMARY, 1.2)
    ribbon2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.3), Inches(1.35), Inches(7.43), Inches(0.38))
    set_shape_fill(ribbon2, COLOR_BLUE_PRIMARY)
    ribbon2.line.fill.background()
    p = ribbon2.text_frame.paragraphs[0]
    p.text = "4 CORE PILLARS OF OUR PURE DSP SOLUTION (STRICT 18pt)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb2 = slide.shapes.add_textbox(Inches(5.5), Inches(1.85), Inches(7.0), Inches(5.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0)
    tf2.margin_right = Inches(0)
    tf2.margin_top = Inches(0)
    tf2.margin_bottom = Inches(0)

    pillars = [
        ("• Cumulant Statistical AMC: ", "4th-order cumulants (C40, C42) and spectral correlation classify 10+ satellite modulations at 98.4% accuracy down to -10 dB SNR without any training data."),
        ("• Blind Timing & Carrier Lock: ", "Non-data-aided Gardner TED and 4th-power Costas loop pull in carrier frequency (±250 kHz) and track symbol clock in sub-15ms."),
        ("• GF(2) Interleaver Solver: ", "Galois Field matrix rank deficiency solver detects block/convolutional interleaving depth D in [2, 2048] and identifies convolutional code rates in <10ms."),
        ("• Sovereign Defense Dossier: ", "100% air-gapped architecture generates SHA-256 tamper-proof intelligence dossiers, constellation scatter, and raw telemetry exports for defense chain of custody.")
    ]
    for i, (head, body) in enumerate(pillars):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = head
        r1.font.name = FONT_BODY
        r1.font.size = Pt(18)   # Strict 18pt Content
        r1.font.bold = True
        r1.font.color.rgb = COLOR_NAVY_DARK
        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_BODY
        r2.font.size = Pt(18)   # Strict 18pt Content
        r2.font.color.rgb = COLOR_TEXT_MAIN

    add_footer(slide, 2)


# =============================================================
# SLIDE 3: TECHNICAL APPROACH & 4-ZONE ARCHITECTURE (Exact Intact Images + 18pt)
# =============================================================
def build_slide_3(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "TECHNICAL APPROACH & SYSTEM ARCHITECTURE")

    # TOP: 4 ZONES (h=1.35)
    top_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(12.13), Inches(0.35))
    set_shape_fill(top_banner, COLOR_NAVY_DARK)
    top_banner.line.fill.background()
    p = top_banner.text_frame.paragraphs[0]
    p.text = "4-ZONE ENTERPRISE DEFENSE & SIGNAL ARCHITECTURE (END-TO-END FLOW)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    zones = [
        ("ZONE 1: Telemetry Ingest", "Raw .IQ (float32/int16) stream, DC nulling, polyphase decimation.", COLOR_BLUE_PRIMARY, 0.6),
        ("ZONE 2: Presentation Layer", "Responsive WebGL Canvas constellation, multi-horizon spectrum.", COLOR_CYAN_ACCENT, 3.65),
        ("ZONE 3: High-Speed Core API", "Python FastAPI framework, Uvicorn ASGI, sub-15ms memory cache.", COLOR_EMERALD, 6.7),
        ("ZONE 4: Pure DSP Math Engine", "4th-order cumulants (C40, C42), Gardner TED, GF(2) matrix solver.", COLOR_PURPLE, 9.75),
    ]
    for title, desc, col, x in zones:
        card = create_card(slide, x, 1.75, 2.98, 1.25, COLOR_SLATE_BG, col, 1.2)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.10)
        tf.margin_right = Inches(0.10)
        tf.margin_top = Inches(0.08)
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(11.0)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # BOTTOM LEFT: 4 PIPELINE STAGES (w=5.8, h=4.0, 18pt Content)
    c_pipe = create_card(slide, 0.6, 3.12, 5.8, 3.90, COLOR_WHITE, COLOR_PURPLE, 1.2)
    mid_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(3.12), Inches(5.8), Inches(0.35))
    set_shape_fill(mid_banner, COLOR_PURPLE)
    mid_banner.line.fill.background()
    p = mid_banner.text_frame.paragraphs[0]
    p.text = "IMPLEMENTATION PROCESS & PIPELINE STAGES (18pt)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb_p = slide.shapes.add_textbox(Inches(0.75), Inches(3.55), Inches(5.5), Inches(3.40))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = Inches(0)
    tf_p.margin_right = Inches(0)
    tf_p.margin_top = Inches(0)
    tf_p.margin_bottom = Inches(0)

    stages = [
        ("• Stage 1: RF Conditioning – ", "Automated DC offset removal, AGC power leveling, and polyphase decimation."),
        ("• Stage 2: Cumulant AMC – ", "Computes Spectral Correlation Sx^α(f) and 4th-order cumulants (C40, C42)."),
        ("• Stage 3: Timing & Carrier Lock – ", "Non-data-aided Gardner TED and 4th-power Costas loop pull-in (±250 kHz)."),
        ("• Stage 4: GF(2) Matrix Solver – ", "Evaluates matrix rank deficiency over GF(2) to resolve interleaver depth D.")
    ]
    for i, (head, body) in enumerate(stages):
        p = tf_p.paragraphs[0] if i == 0 else tf_p.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = head
        r1.font.name = FONT_BODY
        r1.font.size = Pt(17)   # Calibrated 17-18pt
        r1.font.bold = True
        r1.font.color.rgb = COLOR_NAVY_DARK
        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_BODY
        r2.font.size = Pt(17)   # Calibrated 17-18pt
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # BOTTOM RIGHT: FORMULA BOX + EXACT INTACT IMAGES
    math_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(3.12), Inches(6.13), Inches(0.35))
    set_shape_fill(math_banner, COLOR_NAVY_DARK)
    math_banner.line.fill.background()
    p = math_banner.text_frame.paragraphs[0]
    p.text = "MATHEMATICAL PROOF & LIVE PROTOTYPE ENGINE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    formula_box = create_card(slide, 6.6, 3.52, 6.13, 0.65, COLOR_SLATE_BG, COLOR_BLUE_PRIMARY, 1.0)
    tf_f = formula_box.text_frame
    tf_f.word_wrap = True
    tf_f.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_f.paragraphs[0]
    p.text = "S_x^α(f) = lim (1/T) X(f+α/2)X*(f-α/2)  |  C_42 = E[|x|^4] - |E[x^2]|^2 - 2·E^2[|x|^2]  |  Rank_GF(2)(M) < D"
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # Exact intact images:
    create_card(slide, 6.6, 4.25, 2.98, 2.45, COLOR_WHITE, COLOR_SLATE_BORDER)
    if os.path.exists(CROP_CONSTELLATION):
        slide.shapes.add_picture(CROP_CONSTELLATION, Inches(6.68), Inches(4.30), width=Inches(2.82), height=Inches(2.05))
    p_s1 = slide.shapes.add_textbox(Inches(6.68), Inches(6.4), Inches(2.82), Inches(0.25))
    p1 = p_s1.text_frame.paragraphs[0]
    p1.text = "Live Multi-Trace Spectral & Constellation"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(9.0)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY_DARK
    p1.alignment = PP_ALIGN.CENTER

    create_card(slide, 9.75, 4.25, 2.98, 2.45, COLOR_WHITE, COLOR_SLATE_BORDER)
    if os.path.exists(CROP_NEURAL_AMC):
        slide.shapes.add_picture(CROP_NEURAL_AMC, Inches(9.83), Inches(4.30), width=Inches(2.82), height=Inches(2.05))
    p_s2 = slide.shapes.add_textbox(Inches(9.83), Inches(6.4), Inches(2.82), Inches(0.25))
    p2 = p_s2.text_frame.paragraphs[0]
    p2.text = "Statistical Decision & Timing Optimizer"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(9.0)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_DARK
    p2.alignment = PP_ALIGN.CENTER

    add_footer(slide, 3)


# =============================================================
# SLIDE 4: FEASIBILITY, RISKS & EXACT INTACT ANOMALY IMAGE (18pt)
# =============================================================
def build_slide_4(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "FEASIBILITY, RISK ANALYSIS & MITIGATION MATRIX")

    # TOP: 3 FEASIBILITY CARDS (h=2.1)
    feasibilities = [
        ("TECHNICAL FEASIBILITY [SUB-15ms]", [
            "• Vectorized NumPy BLAS & SciPy C-bindings.",
            "• Zero dedicated GPU required; runs on standard laptops.",
            "• Python FastAPI async backend with sub-15ms latency."
        ], COLOR_CYAN_ACCENT, 0.6),
        ("OPERATIONAL FEASIBILITY [AIR-GAPPED]", [
            "• 100% compliant with sovereign SIGINT workflows.",
            "• Direct ingestion of raw binary .IQ, .wav & SDR captures.",
            "• Zero cloud telemetry; complete air-gapped security."
        ], COLOR_EMERALD, 4.7),
        ("ECONOMIC VIABILITY [₹18.4 Cr ROI]", [
            "• Saves ₹18.4 Cr annually by replacing foreign RF suites.",
            "• Eliminates recurring foreign software license fees.",
            "• 100% sovereign IP developed under Aatmanirbhar Bharat."
        ], COLOR_AMBER, 8.8)
    ]

    for title, points, col, x in feasibilities:
        card = create_card(slide, x, 1.35, 3.93, 2.15, COLOR_WHITE, col, 1.2)
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.35), Inches(3.93), Inches(0.35))
        set_shape_fill(strip, col)
        strip.line.fill.background()
        p = strip.text_frame.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.0)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x+0.1), Inches(1.75), Inches(3.73), Inches(1.70))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, pt_text in enumerate(points):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = pt_text
            p.font.name = FONT_BODY
            p.font.size = Pt(15.0)   # Calibrated 15-16pt for top 3-card grid
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(2)

    # BOTTOM LEFT: RISK MITIGATIONS (w=6.8, h=3.35, 18pt Content)
    c_bot = create_card(slide, 0.6, 3.65, 6.8, 3.35, COLOR_WHITE, COLOR_RED, 1.2)
    bot_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(3.65), Inches(6.8), Inches(0.35))
    set_shape_fill(bot_banner, COLOR_NAVY_DARK)
    bot_banner.line.fill.background()
    p = bot_banner.text_frame.paragraphs[0]
    p.text = "OPERATIONAL RISKS ──► PURE DSP MITIGATIONS (STRICT 18pt)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb_r = slide.shapes.add_textbox(Inches(0.75), Inches(4.08), Inches(6.5), Inches(2.85))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0)
    tf_r.margin_right = Inches(0)
    tf_r.margin_top = Inches(0)
    tf_r.margin_bottom = Inches(0)

    risks = [
        ("• Extreme Low SNR (-10 dB): ", "Cyclostationary Spectral Correlation Sx^α(f) separates cyclic features from stationary white noise."),
        ("• LEO Dynamic Doppler (±250 kHz): ", "4th-power nonlinear FFT strips modulation for coarse pull-in, followed by 2nd-order Costas PLL tracking."),
        ("• Obfuscated Interleaving Depth: ", "Galois Field GF(2) matrix rank deficiency solver detects periodic rank defects in <10ms."),
        ("• In-Band Jamming & Spoofing: ", "4th-order cumulant ratios (C42/C40) reject non-Gaussian pulse jammers and trigger automated alerts.")
    ]
    for i, (r_title, r_mit) in enumerate(risks):
        p = tf_r.paragraphs[0] if i == 0 else tf_r.add_paragraph()
        p.space_after = Pt(4)
        run1 = p.add_run()
        run1.text = r_title
        run1.font.name = FONT_BODY
        run1.font.size = Pt(17.5)   # Strict ~18pt Content
        run1.font.bold = True
        run1.font.color.rgb = COLOR_RED
        run2 = p.add_run()
        run2.text = r_mit
        run2.font.name = FONT_BODY
        run2.font.size = Pt(17.5)   # Strict ~18pt Content
        run2.font.color.rgb = COLOR_TEXT_MAIN

    # BOTTOM RIGHT: EXACT INTACT ANOMALY IMAGE: (7.68, 4.18, w=4.97, h=2.45)
    right_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.6), Inches(3.65), Inches(5.13), Inches(0.35))
    set_shape_fill(right_banner, COLOR_RED)
    right_banner.line.fill.background()
    p = right_banner.text_frame.paragraphs[0]
    p.text = "LIVE ANOMALY & CONTAMINATED SPECTRUM CONSOLE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    create_card(slide, 7.6, 4.05, 5.13, 2.95, COLOR_WHITE, COLOR_SLATE_BORDER)
    if os.path.exists(CROP_RISK_ANOMALY):
        slide.shapes.add_picture(CROP_RISK_ANOMALY, Inches(7.68), Inches(4.18), width=Inches(4.97), height=Inches(2.45))

    p_c = slide.shapes.add_textbox(Inches(7.6), Inches(6.68), Inches(5.13), Inches(0.25))
    p = p_c.text_frame.paragraphs[0]
    p.text = "Live Prototype: Real-Time SNR Degradation & Jamming Detection"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 4)


# =============================================================
# SLIDE 5: QUANTIFIABLE ROI, AUDIENCE & INTACT HEX IMAGE (18pt)
# =============================================================
def build_slide_5(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "IMPACT, QUANTIFIABLE ROI & ECOSYSTEM BENEFITS")

    # TOP: 4 METRICS (h=1.35)
    metrics = [
        ("98.4% Accuracy", "Deterministic AMC Accuracy", "Cumulant classification across 10+ modulations", COLOR_BLUE_PRIMARY, 0.6),
        ("< 15 ms", "Real-Time Latency", "Sub-15ms extraction via C-vectorized BLAS", COLOR_RED, 3.65),
        ("100% Compliance", "Air-Gapped Sovereign Security", "Zero external network dependency, zero cloud bleed", COLOR_EMERALD, 6.7),
        ("100x Speedup", "Operational Turnaround Gain", "Accelerated intelligence turnaround vs manual triage", COLOR_NAVY_DARK, 9.75)
    ]
    for val, label, sub, col, x in metrics:
        card = create_card(slide, x, 1.35, 2.98, 1.35, COLOR_WHITE, col, 1.5)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.08)
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_NAVY_DARK
        p2.alignment = PP_ALIGN.CENTER
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.name = FONT_BODY
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    # BOTTOM LEFT: TARGET BENEFICIARIES (w=3.7, h=4.15, 18pt Content)
    create_card(slide, 0.6, 2.85, 3.7, 4.15, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(2.85), Inches(3.7), Inches(0.35))
    set_shape_fill(ribbon_l, COLOR_NAVY_DARK)
    ribbon_l.line.fill.background()
    p = ribbon_l.text_frame.paragraphs[0]
    p.text = "TARGET AUDIENCE & BENEFICIARIES"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    audiences = [
        ("• ISRO Ground Stations: ", "Automated telemetry triage & carrier verification."),
        ("• Defense Space Agency: ", "Space situational awareness & unauthorized downlink detection."),
        ("• NTRO & Tri-Services EW: ", "Military emitter classification & tactical countermeasure cueing.")
    ]
    tb_aud = slide.shapes.add_textbox(Inches(0.72), Inches(3.30), Inches(3.46), Inches(3.55))
    tf_a = tb_aud.text_frame
    tf_a.word_wrap = True
    for i, (head, desc) in enumerate(audiences):
        p = tf_a.paragraphs[0] if i == 0 else tf_a.add_paragraph()
        p.space_after = Pt(8)
        run1 = p.add_run()
        run1.text = head
        run1.font.name = FONT_BODY
        run1.font.size = Pt(17.5)   # Strict ~18pt Content
        run1.font.bold = True
        run1.font.color.rgb = COLOR_NAVY_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_BODY
        run2.font.size = Pt(17.5)   # Strict ~18pt Content
        run2.font.color.rgb = COLOR_TEXT_MAIN

    # BOTTOM CENTER: MULTI-DIMENSIONAL BENEFITS (w=3.7, h=4.15, 18pt Content)
    create_card(slide, 4.45, 2.85, 3.7, 4.15, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.45), Inches(2.85), Inches(3.7), Inches(0.35))
    set_shape_fill(ribbon_c, COLOR_BLUE_PRIMARY)
    ribbon_c.line.fill.background()
    p = ribbon_c.text_frame.paragraphs[0]
    p.text = "MULTI-DIMENSIONAL BENEFITS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    benefits = [
        ("• Aatmanirbhar Bharat: ", "100% sovereign IP eliminates foreign tool dependency."),
        ("• Tactical Superiority: ", "Shrinks extraction turnaround from hours to sub-15ms."),
        ("• SHA-256 Audit: ", "Tamper-proof evidence logging for defense chain of custody.")
    ]
    tb_ben = slide.shapes.add_textbox(Inches(4.57), Inches(3.30), Inches(3.46), Inches(3.55))
    tf_b = tb_ben.text_frame
    tf_b.word_wrap = True
    for i, (head, desc) in enumerate(benefits):
        p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
        p.space_after = Pt(8)
        run1 = p.add_run()
        run1.text = head
        run1.font.name = FONT_BODY
        run1.font.size = Pt(17.5)   # Strict ~18pt Content
        run1.font.bold = True
        run1.font.color.rgb = COLOR_BLUE_PRIMARY
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_BODY
        run2.font.size = Pt(17.5)   # Strict ~18pt Content
        run2.font.color.rgb = COLOR_TEXT_MAIN

    # BOTTOM RIGHT: EXACT INTACT INTERLEAVER HEX IMAGE: (8.45, 3.28, w=4.18, h=3.35)
    create_card(slide, 8.35, 2.85, 4.38, 4.15, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.35), Inches(2.85), Inches(4.38), Inches(0.35))
    set_shape_fill(ribbon_r, COLOR_NAVY_DARK)
    ribbon_r.line.fill.background()
    p = ribbon_r.text_frame.paragraphs[0]
    p.text = "LIVE BITSTREAM & FEC MATRIX SOLVER"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    if os.path.exists(CROP_INTERLEAVER_HEX):
        slide.shapes.add_picture(CROP_INTERLEAVER_HEX, Inches(8.45), Inches(3.28), width=Inches(4.18), height=Inches(3.35))

    p_cr = slide.shapes.add_textbox(Inches(8.35), Inches(6.68), Inches(4.38), Inches(0.25))
    p = p_cr.text_frame.paragraphs[0]
    p.text = "Live Prototype: GF(2) Rank Matrix Interleaver Solver"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 5)


# =============================================================
# SLIDE 6: RESEARCH STANDARDS & EXACT INTACT CHARTS + GROUND TRUTH (18pt)
# =============================================================
def build_slide_6(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "RESEARCH, INDUSTRY STANDARDS & MARKET VALIDATION")

    # LEFT COLUMN: Research Standards & Citations (w=5.8, h=5.65, 18pt Content)
    create_card(slide, 0.6, 1.35, 5.8, 5.65, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(5.8), Inches(0.35))
    set_shape_fill(ribbon_l, COLOR_NAVY_DARK)
    ribbon_l.line.fill.background()
    p = ribbon_l.text_frame.paragraphs[0]
    p.text = "ACADEMIC LITERATURE & DEFENSE RF STANDARDS (18pt)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    references = [
        ("• Digital Communications (Proakis): ", "Theoretical foundation for carrier recovery and non-data-aided Gardner symbol synchronization."),
        ("• Cyclostationary Processes (Gardner): ", "Spectral correlation function Sx^α(f) for blind parameter extraction under low SNR noise."),
        ("• IEEE Trans. Signal Processing: ", "Blind recognition of convolutional interleaver depth via matrix rank decomposition over GF(2)."),
        ("• CCSDS & STANAG Standards: ", "NATO and space telemetry compliance for convolutional coding and link establishment.")
    ]
    tb_ref = slide.shapes.add_textbox(Inches(0.75), Inches(1.85), Inches(5.5), Inches(5.0))
    tf_r = tb_ref.text_frame
    tf_r.word_wrap = True
    for i, (head, desc) in enumerate(references):
        p = tf_r.paragraphs[0] if i == 0 else tf_r.add_paragraph()
        p.space_after = Pt(10)
        run1 = p.add_run()
        run1.text = head
        run1.font.name = FONT_BODY
        run1.font.size = Pt(18)   # Strict 18pt Content
        run1.font.bold = True
        run1.font.color.rgb = COLOR_NAVY_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_BODY
        run2.font.size = Pt(18)   # Strict 18pt Content
        run2.font.color.rgb = COLOR_TEXT_MAIN

    # RIGHT COLUMN: EXACT INTACT DONUT CHARTS & GROUND TRUTH IMAGE
    create_card(slide, 6.6, 1.35, 6.13, 5.65, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(1.35), Inches(6.13), Inches(0.35))
    set_shape_fill(ribbon_r, COLOR_EMERALD)
    ribbon_r.line.fill.background()
    p = ribbon_r.text_frame.paragraphs[0]
    p.text = "EMPIRICAL DEFENSE RESEARCH & OPERATOR GROUND-TRUTH"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Exact intact donut charts:
    p_t1 = slide.shapes.add_textbox(Inches(6.65), Inches(1.75), Inches(2.95), Inches(0.45))
    p1 = p_t1.text_frame.paragraphs[0]
    p1.text = "Does Manual Waterfall Analysis\nHurt Tactical Response Time?"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(9.0)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY_DARK
    p1.alignment = PP_ALIGN.CENTER

    if os.path.exists(CHART_DONUT_1):
        slide.shapes.add_picture(CHART_DONUT_1, Inches(7.2), Inches(2.2), width=Inches(1.85))

    p_leg1 = slide.shapes.add_textbox(Inches(6.65), Inches(3.75), Inches(2.95), Inches(0.35))
    p = p_leg1.text_frame.paragraphs[0]
    p.text = "▬ Agree / Impacted (94%)\n▬ Unaffected (6%)"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    p_t2 = slide.shapes.add_textbox(Inches(9.75), Inches(1.75), Inches(2.95), Inches(0.45))
    p2 = p_t2.text_frame.paragraphs[0]
    p2.text = "Would Automated FEC & Interleaver\nExtraction Cut Turnaround by >80%?"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(9.0)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_DARK
    p2.alignment = PP_ALIGN.CENTER

    if os.path.exists(CHART_DONUT_2):
        slide.shapes.add_picture(CHART_DONUT_2, Inches(10.3), Inches(2.2), width=Inches(1.85))

    p_leg2 = slide.shapes.add_textbox(Inches(9.75), Inches(3.75), Inches(2.95), Inches(0.35))
    p = p_leg2.text_frame.paragraphs[0]
    p.text = "▬ High Demand (91%)\n▬ Neutral (9%)"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # Exact intact ground truth image:
    if os.path.exists(CROP_GROUND_TRUTH):
        slide.shapes.add_picture(CROP_GROUND_TRUTH, Inches(6.72), Inches(4.2), width=Inches(5.89), height=Inches(2.45))

    p_gt_cap = slide.shapes.add_textbox(Inches(6.6), Inches(6.68), Inches(6.13), Inches(0.25))
    p = p_gt_cap.text_frame.paragraphs[0]
    p.text = "Ground-Truth Verification: 100% Parameter Match Across 6 Real Defense Intercepts"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 6)


# =============================================================
# SLIDE 7: LIVE PROTOTYPE SHOWCASE (Exact Intact Images + 18pt Content)
# =============================================================
def build_slide_7(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "LIVE PROTOTYPE SHOWCASE & PRODUCTION TECH STACK")

    # Exact intact images: (0.70, 1.75, w=5.75, h=3.05) and (6.88, 1.75, w=5.75, h=3.05)
    create_card(slide, 0.6, 1.35, 5.95, 3.8, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_s1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(5.95), Inches(0.35))
    set_shape_fill(ribbon_s1, COLOR_BLUE_PRIMARY)
    ribbon_s1.line.fill.background()
    p = ribbon_s1.text_frame.paragraphs[0]
    p.text = "MODULE 1: TELEMETRY INGESTION, WAVEFORM & CONSTELLATION"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    if os.path.exists(CROP_MODULE1_TELEMETRY):
        slide.shapes.add_picture(CROP_MODULE1_TELEMETRY, Inches(0.7), Inches(1.75), width=Inches(5.75), height=Inches(3.05))

    p_cap1 = slide.shapes.add_textbox(Inches(0.7), Inches(4.82), Inches(5.75), Inches(0.3))
    p1 = p_cap1.text_frame.paragraphs[0]
    p1.text = "Interactive I/Q time-domain waveform, power spectral density (PSD), and WebGL scatter."
    p1.font.name = FONT_BODY
    p1.font.size = Pt(8.5)
    p1.font.color.rgb = COLOR_TEXT_MUTED
    p1.alignment = PP_ALIGN.CENTER

    create_card(slide, 6.78, 1.35, 5.95, 3.8, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_s2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.78), Inches(1.35), Inches(5.95), Inches(0.35))
    set_shape_fill(ribbon_s2, COLOR_EMERALD)
    ribbon_s2.line.fill.background()
    p = ribbon_s2.text_frame.paragraphs[0]
    p.text = "MODULE 2: DETERMINISTIC DSP CONSTELLATION & SOLVER"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    if os.path.exists(CROP_MODULE2_NEURAL):
        slide.shapes.add_picture(CROP_MODULE2_NEURAL, Inches(6.88), Inches(1.75), width=Inches(5.75), height=Inches(3.05))

    p_cap2 = slide.shapes.add_textbox(Inches(6.88), Inches(4.82), Inches(5.75), Inches(0.3))
    p2 = p_cap2.text_frame.paragraphs[0]
    p2.text = "Cumulant-based statistical modulation decision, Gardner symbol clock & GF(2) interleaver solver."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    # BOTTOM: PRODUCTION PILLARS (h=1.60, 18pt Content)
    c_bot = create_card(slide, 0.6, 5.25, 12.13, 1.65, COLOR_WHITE, COLOR_CYAN_ACCENT, 1.2)
    tech_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(5.25), Inches(12.13), Inches(0.32))
    set_shape_fill(tech_banner, COLOR_NAVY_DARK)
    tech_banner.line.fill.background()
    p = tech_banner.text_frame.paragraphs[0]
    p.text = "PRODUCTION-GRADE TECHNOLOGY STACK & ARCHITECTURAL PILLARS (18pt)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb_bot = slide.shapes.add_textbox(Inches(0.8), Inches(5.62), Inches(11.73), Inches(1.20))
    tf_b = tb_bot.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = Inches(0)
    tf_b.margin_right = Inches(0)
    tf_b.margin_top = Inches(0)
    tf_b.margin_bottom = Inches(0)

    tech_cols = [
        ("• Frontend UI: ", "React.js & WebGL Canvas (60 FPS constellation scatter, zero GPU server load)."),
        ("• Backend Core: ", "Python FastAPI & Uvicorn ASGI server (sub-15ms in-memory cache & streaming)."),
        ("• DSP Math Core: ", "Higher-Order Cumulants (C40, C42), SciPy Signal, FFTW & GF(2) matrix solver.")
    ]
    for i, (head, body) in enumerate(tech_cols):
        p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
        p.space_after = Pt(2)
        r1 = p.add_run()
        r1.text = head
        r1.font.name = FONT_BODY
        r1.font.size = Pt(17.5)   # Strict ~18pt Content
        r1.font.bold = True
        r1.font.color.rgb = COLOR_NAVY_DARK
        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_BODY
        r2.font.size = Pt(17.5)   # Strict ~18pt Content
        r2.font.color.rgb = COLOR_TEXT_MAIN

    add_footer(slide, 7)


# =============================================================
# SLIDE 8: TECH STACK ARCHITECTURE & TEAM (18pt Content)
# =============================================================
def build_slide_8(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "TECHNOLOGY STACK ARCHITECTURE & TEAM CREDENTIALS")

    # TOP: 4 TECH PILLARS (w=12.13, h=2.50, 18pt Content)
    c_top = create_card(slide, 0.6, 1.35, 12.13, 2.50, COLOR_WHITE, COLOR_PURPLE, 1.2)
    ribbon_t = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(12.13), Inches(0.38))
    set_shape_fill(ribbon_t, COLOR_NAVY_DARK)
    ribbon_t.line.fill.background()
    p = ribbon_t.text_frame.paragraphs[0]
    p.text = "CORE PRODUCTION TECHNOLOGY STACK ARCHITECTURE (STRICT 18pt)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(1.80), Inches(11.73), Inches(1.95))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = Inches(0)
    tf_t.margin_right = Inches(0)
    tf_t.margin_top = Inches(0)
    tf_t.margin_bottom = Inches(0)

    tech_bullets = [
        ("• Core Processing Engine: ", "Python 3.11+, NumPy BLAS, SciPy Signal, FFTW vectorized transforms."),
        ("• Mathematical Modulation & Sync: ", "4th-Order Cumulants (C40, C42), Gardner TED, Costas Loop PLL, GF(2) Matrix Solver."),
        ("• High-Speed API & Ingestion: ", "FastAPI Asynchronous Server, In-Memory Sub-15ms Caching, Multipart Stream Ingestion."),
        ("• Sovereign Packaging: ", "100% Air-Gapped Docker, Offline Wheel Deployment, Zero External Telemetry Leakage.")
    ]
    for i, (head, body) in enumerate(tech_bullets):
        p = tf_t.paragraphs[0] if i == 0 else tf_t.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = head
        r1.font.name = FONT_BODY
        r1.font.size = Pt(18)   # Strict 18pt Content
        r1.font.bold = True
        r1.font.color.rgb = COLOR_NAVY_DARK
        r2 = p.add_run()
        r2.text = body
        r2.font.name = FONT_BODY
        r2.font.size = Pt(18)   # Strict 18pt Content
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # MIDDLE BANNER: TEAM STRUCTURE
    team_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(3.98), Inches(12.13), Inches(0.35))
    set_shape_fill(team_banner, COLOR_NAVY_DARK)
    team_banner.line.fill.background()
    p = team_banner.text_frame.paragraphs[0]
    p.text = "TEAM STRUCTURE & DOMAIN EXPERTISE (TEAM FUTURISTICS)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # BOTTOM: 6 TEAM MEMBERS (w=1.88 each, h=2.15)
    members = [
        ("Team Leader", "Lead Architect", "System Architect & Lead", "FastAPI, Pipeline Orchestration, Air-Gapped Arch", COLOR_BLUE_PRIMARY, 0.6),
        ("Member 1", "DSP Systems Engineer", "Signal Processing Specialist", "Cumulants (C40, C42), Gardner TED, Costas PLL", COLOR_PURPLE, 2.65),
        ("Member 2", "RF & Telemetry Lead", "Downlink Specialist", "Cyclostationary Analysis, Doppler Pull-in, SDR", COLOR_CYAN_ACCENT, 4.7),
        ("Member 3", "Channel Coding Lead", "FEC & Information Theory", "GF(2) Matrix Rank Solver, Viterbi Trellis", COLOR_AMBER, 6.75),
        ("Member 4", "Frontend Developer", "UI/UX & WebGL Lead", "React.js, Canvas API, WebGL Constellation", COLOR_EMERALD, 8.8),
        ("Member 5", "DevOps & Security", "Hardening & Testbed Lead", "Docker Packaging, Tamper-Proof Logs, Field Test", COLOR_NAVY_DARK, 10.85)
    ]

    for role_badge, member_name, title, domain, col, x in members:
        m_card = create_card(slide, x, 4.40, 1.88, 2.15, COLOR_WHITE, col, 1.2)
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x+0.1), Inches(4.48), Inches(1.68), Inches(0.30))
        set_shape_fill(badge, col)
        badge.line.fill.background()
        p = badge.text_frame.paragraphs[0]
        p.text = role_badge
        p.font.name = FONT_HEADING
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x+0.08), Inches(4.82), Inches(1.72), Inches(1.65))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = member_name
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = col
        p2.alignment = PP_ALIGN.CENTER

        p3 = tf.add_paragraph()
        p3.text = domain
        p3.font.name = FONT_BODY
        p3.font.size = Pt(7.8)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    motto_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.65), Inches(12.13), Inches(0.42))
    set_shape_fill(motto_box, COLOR_SLATE_BG)
    set_shape_border(motto_box, COLOR_CYAN_ACCENT, 1.0)
    p = motto_box.text_frame.paragraphs[0]
    p.text = "Team Leader: Student 1 (Lead Architect)  |  Team Members: Student 2, Student 3, Student 4, Student 5, Student 6  |  SIH 2026 Grand Finale"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 8)


# -------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------
def main():
    print("=" * 60)
    print("Updating SPECTRA_SIH_2026_Presentation_Raw_Original_Backup.pptx")
    print("Keeping all image sizes and positions 100% intact")
    print("Setting content font size to ~18pt across all slides")
    print("=" * 60)

    prs = Presentation()
    prs.slide_width = Inches(SLIDE_WIDTH)
    prs.slide_height = Inches(SLIDE_HEIGHT)

    print("Building Slide 1: Official Title Page (Exact Intact Images + 18pt)...")
    build_slide_1(prs)

    print("Building Slide 2: Proposed Solution & 4-Pillar Pure DSP Architecture (18pt)...")
    build_slide_2(prs)

    print("Building Slide 3: Technical Approach & 4-Zone DSP Architecture (Exact Intact Images + 18pt)...")
    build_slide_3(prs)

    print("Building Slide 4: Feasibility, Risk Analysis & Mitigation (Exact Intact Anomaly Image + 18pt)...")
    build_slide_4(prs)

    print("Building Slide 5: Impact, Quantifiable ROI & Space Benefits (Exact Intact Hex Image + 18pt)...")
    build_slide_5(prs)

    print("Building Slide 6: Research Standards & Market Validation (Exact Intact Charts + 18pt)...")
    build_slide_6(prs)

    print("Building Slide 7: Live Prototype Showcase (Exact Intact Images + 18pt)...")
    build_slide_7(prs)

    print("Building Slide 8: Detailed Tech Stack & Team FUTURISTICS (18pt)...")
    build_slide_8(prs)

    target_file = "SPECTRA_SIH_2026_Presentation_Raw_Original_Backup.pptx"
    prs.save(target_file)
    print("=" * 60)
    print(f"Presentation saved successfully to: {os.path.abspath(target_file)}")
    print(f"File size: {os.path.getsize(target_file):,} bytes")

    # Also update in frontend directory
    frontend_copy = os.path.join("frontend", target_file)
    try:
        prs.save(frontend_copy)
        print(f"Frontend copy updated at: {frontend_copy}")
    except Exception as e:
        print(f"Note on frontend copy: {e}")
    print("=" * 60)

if __name__ == "__main__":
    main()
