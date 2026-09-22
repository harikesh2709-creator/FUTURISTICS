"""
SPECTRA / FUTURISTICS - Official Smart India Hackathon (SIH 2026) PowerPoint Presentation Generator
Version 2: Fully packed with zero whitespace, real charts (donut graphs), embedded UI screenshots,
and matching the exact layout and details of the user's reference winning SIH submission.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
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
COLOR_PURPLE = RGBColor(124, 58, 237)        # #7C3AED - AI & Math
COLOR_PURPLE_BG = RGBColor(245, 243, 255)    # #F5F3FF - Purple tint
COLOR_SLATE_BG = RGBColor(248, 250, 252)     # #F8FAFC - Card background
COLOR_SLATE_BORDER = RGBColor(226, 232, 240) # #E2E8F0 - Card border
COLOR_TEXT_MAIN = RGBColor(15, 23, 42)       # #0F172A - Body text main
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B - Subtitles & labels
COLOR_WHITE = RGBColor(255, 255, 255)        # #FFFFFF - White
COLOR_RED = RGBColor(239, 68, 68)            # #EF4444 - Risks

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

ASSETS_DIR = "presentation_assets"
SIH_HEADER_LOGO = os.path.join(ASSETS_DIR, "sih_header_logo.png")
SIH_BULB_LOGO = os.path.join(ASSETS_DIR, "sih_bulb_logo.png")
CHART_DONUT_1 = os.path.join(ASSETS_DIR, "chart_donut_bottleneck.png")
CHART_DONUT_2 = os.path.join(ASSETS_DIR, "chart_donut_demand.png")

SCREEN_CONSTELLATION = os.path.join(ASSETS_DIR, "screen_constellation.png")
SCREEN_NEURAL_LAB = os.path.join(ASSETS_DIR, "screen_neural_lab.png")
SCREEN_RISK_CONSOLE = os.path.join(ASSETS_DIR, "screen_risk_console.png")
SCREEN_INTERLEAVER = os.path.join(ASSETS_DIR, "screen_interleaver_solver.png")
SCREEN_GROUND_TRUTH = os.path.join(ASSETS_DIR, "screen_ground_truth.png")
SCREEN_MISSION_RADAR = os.path.join(ASSETS_DIR, "screen_mission_radar.png")

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def set_shape_border(shape, color, width=1.0):
    shape.line.color.rgb = color
    shape.line.width = Pt(width)

def set_shape_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def create_card(slide, left, top, width, height, bg_color=COLOR_SLATE_BG, border_color=COLOR_SLATE_BORDER, border_width=1.0):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    set_shape_fill(shape, bg_color)
    if border_color:
        set_shape_border(shape, border_color, border_width)
    else:
        shape.line.fill.background()
    return shape

def add_header(slide, title, category_subtitle="SMART INDIA HACKATHON 2026"):
    # Left team badge pill (exactly matching FUTURISTICS / TEAM ID: SIH-2026 from reference PDF)
    team_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.32), Inches(2.4), Inches(0.92))
    set_shape_fill(team_pill, COLOR_NAVY_PILL)
    set_shape_border(team_pill, COLOR_CYAN_ACCENT, 1.2)
    tf = team_pill.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    p = tf.paragraphs[0]
    p.text = "FUTURISTICS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "TEAM ID: SIH-2026"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = COLOR_CYAN_ACCENT
    p2.alignment = PP_ALIGN.CENTER

    # Title & Subtitle text box
    tb = slide.shapes.add_textbox(Inches(3.2), Inches(0.32), Inches(7.5), Inches(0.92))
    tf2 = tb.text_frame
    tf2.word_wrap = True
    tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf2.margin_left = Inches(0)
    tf2.margin_right = Inches(0)
    tf2.margin_top = Inches(0)
    tf2.margin_bottom = Inches(0)
    
    p_sub = tf2.paragraphs[0]
    p_sub.text = category_subtitle.upper()
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(9.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_BLUE_PRIMARY
    
    p_title = tf2.add_paragraph()
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(18)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY_DARK

    # Right SIH Header Logo
    if os.path.exists(SIH_HEADER_LOGO):
        slide.shapes.add_picture(SIH_HEADER_LOGO, Inches(10.9), Inches(0.22), width=Inches(1.85))

def add_footer(slide, slide_num, total_slides=8):
    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(7.12), Inches(12.13), Inches(0.015))
    set_shape_fill(line, COLOR_SLATE_BORDER)
    line.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(7.15), Inches(12.13), Inches(0.25))
    tf = tb.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = f"TEAM FUTURISTICS • SPECTRA Autonomous RF SIGINT Platform • SIH 2026 Final Round | Slide {slide_num} of {total_slides}"
    p.font.name = FONT_BODY
    p.font.size = Pt(8)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.LEFT

# -------------------------------------------------------------
# SLIDE 1: OFFICIAL TITLE PAGE (MATCHING PDF PAGE 1)
# -------------------------------------------------------------
def build_slide_1(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)

    # Top Left Badge: FUTURISTICS / TEAM ID: SIH-2026
    team_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.55), Inches(2.6), Inches(0.95))
    set_shape_fill(team_pill, COLOR_NAVY_PILL)
    set_shape_border(team_pill, COLOR_CYAN_ACCENT, 1.5)
    tf = team_pill.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p1 = tf.paragraphs[0]
    p1.text = "FUTURISTICS"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = "TEAM ID: SIH-2026"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_CYAN_ACCENT
    p2.alignment = PP_ALIGN.CENTER

    # Main Hackathon Header
    tb_header = slide.shapes.add_textbox(Inches(3.7), Inches(0.52), Inches(6.8), Inches(1.0))
    tf_h = tb_header.text_frame
    tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_h = tf_h.paragraphs[0]
    p_h.text = "SMART INDIA HACKATHON 2026"
    p_h.font.name = FONT_HEADING
    p_h.font.size = Pt(28)
    p_h.font.bold = True
    p_h.font.color.rgb = COLOR_NAVY_DARK

    p_sub = tf_h.add_paragraph()
    p_sub.text = "NATIONAL GRAND FINALE • SOFTWARE EDITION"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(10.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_BLUE_PRIMARY

    # Right SIH Header Logo
    if os.path.exists(SIH_HEADER_LOGO):
        slide.shapes.add_picture(SIH_HEADER_LOGO, Inches(10.8), Inches(0.42), width=Inches(2.0))

    # Center/Right SIH Bulb Logo (large, crisp, exactly like PDF Page 1)
    if os.path.exists(SIH_BULB_LOGO):
        slide.shapes.add_picture(SIH_BULB_LOGO, Inches(7.8), Inches(1.8), width=Inches(4.9))

    # Left Metadata Content Card (densely styled to fill the space cleanly)
    meta_card = create_card(slide, 0.8, 1.8, 6.8, 4.6, COLOR_SLATE_BG, COLOR_SLATE_BORDER)
    
    tb_meta = slide.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(6.3), Inches(4.2))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True

    items = [
        ("• Problem Statement ID", "SIH2026-LOG-01 / NTRO-PS-26147", COLOR_BLUE_PRIMARY),
        ("• Problem Statement Title", "FreightForecast Pro / SPECTRA : AI Freight Forecasting & Blind Signal Parameter Extraction", COLOR_NAVY_DARK),
        ("• Theme", "Smart Logistics / Defense & Maritime Communication Supply Chain", COLOR_TEXT_MAIN),
        ("• PS Category", "Software (Autonomous Strategic AI)", COLOR_TEXT_MAIN),
        ("• Team ID", "[SIH-2026-XXXX]", COLOR_BLUE_PRIMARY),
        ("• Team Name", "FUTURISTICS", COLOR_EMERALD)
    ]

    for i, (label, val, val_color) in enumerate(items):
        p = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        p.space_after = Pt(10)
        run1 = p.add_run()
        run1.text = f"{label} – "
        run1.font.name = FONT_HEADING
        run1.font.size = Pt(13)
        run1.font.bold = True
        run1.font.color.rgb = COLOR_NAVY_DARK

        run2 = p.add_run()
        run2.text = val
        run2.font.name = FONT_BODY
        run2.font.size = Pt(13)
        run2.font.bold = (label in ["• Problem Statement ID", "• Team Name"])
        run2.font.color.rgb = val_color

    # Bottom Pill Banner across the slide
    bottom_banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.55), Inches(11.73), Inches(0.55))
    set_shape_fill(bottom_banner, COLOR_NAVY_PILL)
    set_shape_border(bottom_banner, COLOR_CYAN_ACCENT, 1.0)
    tf_b = bottom_banner.text_frame
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.text = "⚡ Autonomous Decision Engine  •  Triple Exponential Holt-Winters & Cyclostationary Modeling  •  Automated Solver  •  100% Air-Gapped Sovereign AI"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_CYAN_ACCENT
    p_b.alignment = PP_ALIGN.CENTER

    add_footer(slide, 1)

# -------------------------------------------------------------
# SLIDE 2: PROPOSED SOLUTION & 4 PILLARS (MATCHING PDF PAGE 2)
# -------------------------------------------------------------
def build_slide_2(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "FreightForecast Pro / SPECTRA: Predictive Chartering & Route Optimizer")

    # LEFT COLUMN (Width: 4.4 in)
    # 1. Core Intelligence Hub & Decision Pipeline (with connected visual nodes!)
    create_card(slide, 0.6, 1.35, 4.4, 2.7, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(4.4), Inches(0.35))
    set_shape_fill(ribbon1, COLOR_NAVY_DARK)
    ribbon1.line.fill.background()
    p = ribbon1.text_frame.paragraphs[0]
    p.text = "CORE INTELLIGENCE HUB & DECISION PIPELINE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Diagram nodes inside Left Card (exactly matching the circular hub diagram in PDF Page 2!)
    # Top feed node
    n_top = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.9), Inches(1.78), Inches(1.8), Inches(0.48))
    set_shape_fill(n_top, COLOR_BLUE_PRIMARY)
    set_shape_border(n_top, COLOR_CYAN_ACCENT, 1.0)
    p = n_top.text_frame.paragraphs[0]
    p.text = "Global Feeds\n(BDI, Fuel, AIS / RF)"
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Center circle node: VOYAGE / SIGNAL SOLVER ENGINE
    n_center = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(2.1), Inches(2.35), Inches(1.4), Inches(0.85))
    set_shape_fill(n_center, COLOR_NAVY_DARK)
    set_shape_border(n_center, COLOR_CYAN_ACCENT, 2.0)
    p = n_center.text_frame.paragraphs[0]
    p.text = "VOYAGE / SIGNAL\nSOLVER ENGINE"
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Left node: Port Draft & Berth Validation
    n_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.72), Inches(2.45), Inches(1.28), Inches(0.55))
    set_shape_fill(n_left, COLOR_EMERALD)
    n_left.line.fill.background()
    p = n_left.text_frame.paragraphs[0]
    p.text = "Port Draft &\nBerth Validation"
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Right node: Holt-Winters 90-Day AI Forecast
    n_right = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.6), Inches(2.45), Inches(1.3), Inches(0.55))
    set_shape_fill(n_right, COLOR_EMERALD)
    n_right.line.fill.background()
    p = n_right.text_frame.paragraphs[0]
    p.text = "Holt-Winters / AMC\n90-Day AI Forecast"
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Bottom node: $/MT Landed Cost Solver
    n_bot = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.85), Inches(3.3), Inches(1.9), Inches(0.52))
    set_shape_fill(n_bot, COLOR_AMBER)
    n_bot.line.fill.background()
    p = n_bot.text_frame.paragraphs[0]
    p.text = "$/MT Landed Cost\n& Interleaver Solver"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # 2. End-to-End Workflow Pipeline (Bottom Left)
    create_card(slide, 0.6, 4.15, 4.4, 2.85, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(4.15), Inches(4.4), Inches(0.35))
    set_shape_fill(ribbon2, COLOR_BLUE_PRIMARY)
    ribbon2.line.fill.background()
    p = ribbon2.text_frame.paragraphs[0]
    p.text = "END-TO-END WORKFLOW PIPELINE:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    wf_steps = [
        "✓ 1. Ingest Baltic Indices (BDI/BCI/BPI) & Raw Telemetry",
        "✓ 2. Stream Satellite AIS Telematics & Speed Vectors",
        "✓ 3. 90-Day Seasonal Holt-Winters & Cyclostationary Forecast",
        "✓ 4. Astronomical Tidal Draft & Berth Clearance Verification",
        "✓ 5. Optimize Landed $/MT & Issue Contract / Signal Advisory"
    ]
    tb_wf = slide.shapes.add_textbox(Inches(0.72), Inches(4.55), Inches(4.16), Inches(1.8))
    tf_wf = tb_wf.text_frame
    tf_wf.word_wrap = True
    for i, s in enumerate(wf_steps):
        p = tf_wf.paragraphs[0] if i == 0 else tf_wf.add_paragraph()
        p.text = s
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(2.5)

    # Live Feed status ticker inside left bottom
    ticker = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.72), Inches(6.5), Inches(4.16), Inches(0.4))
    set_shape_fill(ticker, COLOR_BLUE_LIGHT)
    set_shape_border(ticker, COLOR_CYAN_ACCENT, 1.0)
    p_tick = ticker.text_frame.paragraphs[0]
    p_tick.text = "LIVE FEEDS: BDI 1,918 (+0.5%) • Cape $25.5K/d • VLSFO $610/MT"
    p_tick.font.name = FONT_HEADING
    p_tick.font.size = Pt(8.5)
    p_tick.font.bold = True
    p_tick.font.color.rgb = COLOR_BLUE_PRIMARY
    p_tick.alignment = PP_ALIGN.CENTER

    # RIGHT COLUMN (Width: 7.5 in)
    # 3. Feature Matrix: Legacy Buying vs FreightForecast Pro / SPECTRA
    create_card(slide, 5.2, 1.35, 7.5, 2.7, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.2), Inches(1.35), Inches(7.5), Inches(0.35))
    set_shape_fill(ribbon3, COLOR_NAVY_DARK)
    ribbon3.line.fill.background()
    p = ribbon3.text_frame.paragraphs[0]
    p.text = "FEATURE MATRIX: LEGACY BUYING vs. FREIGHTFORECAST PRO / SPECTRA"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Table with 5 rows (matching PDF Page 2 table exactly!)
    table_shape = slide.shapes.add_table(5, 3, Inches(5.3), Inches(1.78), Inches(7.3), Inches(2.2))
    table = table_shape.table
    table.columns[0].width = Inches(1.7)
    table.columns[1].width = Inches(2.6)
    table.columns[2].width = Inches(3.0)

    headers = ["Core Dimension", "Legacy Spot Buying Desks", "FreightForecast Pro / AI Engine"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_PILL
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_HEADING
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN_ACCENT

    rows_data = [
        ("Freight Volatility Exposure", "✗ Unhedged spot swings (±35% variance)", "✓ Predictive 90-day Holt-Winters hedging"),
        ("Demurrage Risk Management", "✗ Reactive $15K–$30K/day anchorage bleed", "✓ Live AIS congestion & idle-vessel alerts"),
        ("Riverine Berth Draft Clearance", "✗ Manual estimates; grounding / dead-freight", "✓ Dynamic astronomical tidal tables & UKC check"),
        ("Procurement Optimization", "✗ Disjointed static spreadsheets & hearsay", "✓ Automated $/MT total landed cost solver")
    ]
    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = table.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_SLATE_BG if i % 2 == 0 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(8)
            if j == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_NAVY_DARK
            elif j == 1:
                p.font.color.rgb = COLOR_RED
            else:
                p.font.bold = True
                p.font.color.rgb = COLOR_EMERALD

    # 4. Our 4-Pillar Novel Predictive Solution (Bottom Right)
    create_card(slide, 5.2, 4.15, 7.5, 2.35, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon4 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.2), Inches(4.15), Inches(7.5), Inches(0.35))
    set_shape_fill(ribbon4, COLOR_NAVY_DARK)
    ribbon4.line.fill.background()
    p = ribbon4.text_frame.paragraphs[0]
    p.text = "OUR 4-PILLAR NOVEL PREDICTIVE SOLUTION"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    pillars = [
        ("[92.4% ACC] 90-Day Predictive AI Engine", "Triple Exponential Smoothing (α=0.28, β=0.05, γ=0.62) forecasts seasonal freight rates with 92.4% directional accuracy.", COLOR_CYAN_ACCENT, 5.35, 4.58, 3.5, 0.9),
        ("[100% COMPLIANT] Automated Berth & Draft Engine", "Validates physical vessel LOA (≤229m), beam (≤32.2m) & dynamic astronomical tides (+2.4m UKC) for 100% compliance.", COLOR_EMERALD, 8.95, 4.58, 3.6, 0.9),
        ("[$/MT SOLVER] Landed Cost $/MT Solver", "Minimizes [(Hire×Days) + Bunker + Canal + Dues] / MT across routes: Newcastle➔Paradip ($19.61) vs Hay Point ($23.24).", COLOR_AMBER, 5.35, 5.52, 3.5, 0.9),
        ("[STRATEGIC COA] Contract Timing Advisory", "Evaluates forward volatility bounds to trigger optimal Spot vs. COA fixture timing before seasonal rate surges.", COLOR_PURPLE, 8.95, 5.52, 3.6, 0.9)
    ]
    for title, desc, col, x, y, w, h in pillars:
        p_card = create_card(slide, x, y, w, h, COLOR_SLATE_BG, col, 1.2)
        tf = p_card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.1)
        tf.margin_right = Inches(0.1)
        tf.margin_top = Inches(0.06)
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom 4 Pill Badges (exactly like PDF Page 2!)
    badge_data = [
        ("🌐 Live Web App (PWA Ready)", 5.2),
        ("📡 AIS Fleet Telematics Stream", 7.1),
        ("⚡ FastAPI REST Core (<35ms)", 9.0),
        ("📊 Multi-Corridor Analytics", 10.9)
    ]
    for b_text, bx in badge_data:
        b_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(bx), Inches(6.58), Inches(1.8), Inches(0.35))
        set_shape_fill(b_box, COLOR_WHITE)
        set_shape_border(b_box, COLOR_BLUE_PRIMARY, 1.0)
        p = b_box.text_frame.paragraphs[0]
        p.text = b_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE_PRIMARY
        p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 2)

# -------------------------------------------------------------
# SLIDE 3: TECHNICAL APPROACH & SYSTEM ARCHITECTURE (MATCHING PDF PAGE 3)
# -------------------------------------------------------------
def build_slide_3(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "TECHNICAL APPROACH & SYSTEM ARCHITECTURE")

    # TOP: 4-ZONE ENTERPRISE MARITIME ARCHITECTURE
    top_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(12.13), Inches(0.35))
    set_shape_fill(top_banner, COLOR_NAVY_DARK)
    top_banner.line.fill.background()
    p = top_banner.text_frame.paragraphs[0]
    p.text = "4-ZONE ENTERPRISE MARITIME & DEFENSE ARCHITECTURE (END-TO-END FLOW)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    zones = [
        ("ZONE 1: Telemetry & Ingestion", "Baltic Exchange BDI/BCI/BPI feeds, Satellite AIS vessel tracking, Major Port circulars.", COLOR_BLUE_PRIMARY, 0.6),
        ("ZONE 2: Presentation Layer", "React 19 / Next.js SPA, Chart.js multi-horizon curves, Leaflet.js interactive GIS map.", COLOR_CYAN_ACCENT, 3.65),
        ("ZONE 3: High-Speed Core API", "Python FastAPI asynchronous framework, Uvicorn ASGI, Redis In-Memory sub-35ms Cache.", COLOR_EMERALD, 6.7),
        ("ZONE 4: AI & Math Engine", "Statsmodels Holt-Winters, 10,000 Monte Carlo runs, Landed $/MT solver, UKC tidal check.", COLOR_PURPLE, 9.75),
    ]
    for title, desc, col, x in zones:
        card = create_card(slide, x, 1.75, 2.98, 1.25, COLOR_SLATE_BG, col, 1.2)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.12)
        tf.margin_right = Inches(0.12)
        tf.margin_top = Inches(0.1)
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # MIDDLE LEFT: IMPLEMENTATION PROCESS & PIPELINE STAGES (Width: 5.8 in)
    mid_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(3.12), Inches(5.8), Inches(0.35))
    set_shape_fill(mid_banner, COLOR_NAVY_DARK)
    mid_banner.line.fill.background()
    p = mid_banner.text_frame.paragraphs[0]
    p.text = "IMPLEMENTATION PROCESS & PIPELINE STAGES"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    stages = [
        ("[STAGE 1] Data Harmonization & ETL", "Aggregates 1,825 daily Baltic records with live Port Trust draft circulars into schema-validated PostgreSQL tables.", COLOR_BLUE_PRIMARY, 0.6, 3.52, 5.8, 0.85),
        ("[STAGE 2] Triple Seasonal Decomposition", "Holt-Winters isolates monsoon & commodity cycles: Level ℓ(t), Trend b(t), Seasonal s(t) with MAPE 1.7%.", COLOR_PURPLE, 0.6, 4.42, 5.8, 0.85),
        ("[STAGE 3] Physical Berth Draught Safety", "Validates dynamic Under-Keel Clearance: UKC = (Charted Depth + Astronomical Tide) - Arrival Draft ≥ 1.5m.", COLOR_EMERALD, 0.6, 5.32, 5.8, 0.85),
        ("[STAGE 4] Decision Advisory & Contract Hedging", "Mixed Integer Solver ranks $/MT landed cost across corridors; recommends optimal Spot vs COA forward fixtures.", COLOR_AMBER, 0.6, 6.22, 5.8, 0.85)
    ]
    for title, desc, col, x, y, w, h in stages:
        card = create_card(slide, x, y, w, h, COLOR_WHITE, col, 1.2)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.12)
        tf.margin_right = Inches(0.12)
        tf.margin_top = Inches(0.06)
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # MIDDLE RIGHT: MATHEMATICAL FORMULATION & LIVE PROTOTYPE ENGINE (Width: 6.13 in)
    math_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(3.12), Inches(6.13), Inches(0.35))
    set_shape_fill(math_banner, COLOR_NAVY_DARK)
    math_banner.line.fill.background()
    p = math_banner.text_frame.paragraphs[0]
    p.text = "MATHEMATICAL FORMULATION & LIVE PROTOTYPE ENGINE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Formula card (top of right section)
    formula_box = create_card(slide, 6.6, 3.52, 6.13, 0.65, COLOR_SLATE_BG, COLOR_BLUE_PRIMARY, 1.0)
    tf_f = formula_box.text_frame
    tf_f.word_wrap = True
    tf_f.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_f.paragraphs[0]
    p.text = "Holt-Winters: Y(t+h) = [ℓ(t) + h·b(t)] × s(t+h-m)  |  Min $/MT = [(Hire×Days) + Fuel + Dues] ÷ Cargo MT"
    p.font.name = "Consolas"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # TWO REAL SCREENSHOTS EMBEDDED SIDE BY SIDE! (Exactly like PDF Page 3!)
    create_card(slide, 6.6, 4.25, 2.98, 2.45, COLOR_WHITE, COLOR_SLATE_BORDER)
    if os.path.exists(SCREEN_CONSTELLATION):
        slide.shapes.add_picture(SCREEN_CONSTELLATION, Inches(6.68), Inches(4.32), width=Inches(2.82), height=Inches(2.05))
    p_s1 = slide.shapes.add_textbox(Inches(6.68), Inches(6.4), Inches(2.82), Inches(0.25))
    p1 = p_s1.text_frame.paragraphs[0]
    p1.text = "Live Multi-Route Draught Matrix"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(7.5)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY_DARK
    p1.alignment = PP_ALIGN.CENTER

    create_card(slide, 9.75, 4.25, 2.98, 2.45, COLOR_WHITE, COLOR_SLATE_BORDER)
    if os.path.exists(SCREEN_NEURAL_LAB):
        slide.shapes.add_picture(SCREEN_NEURAL_LAB, Inches(9.83), Inches(4.32), width=Inches(2.82), height=Inches(2.05))
    p_s2 = slide.shapes.add_textbox(Inches(9.83), Inches(6.4), Inches(2.82), Inches(0.25))
    p2 = p_s2.text_frame.paragraphs[0]
    p2.text = "Suez vs Cape Canal Optimizer"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(7.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_DARK
    p2.alignment = PP_ALIGN.CENTER

    add_footer(slide, 3)

# -------------------------------------------------------------
# SLIDE 4: FEASIBILITY, RISK ANALYSIS & MITIGATION MATRIX (MATCHING PDF PAGE 4)
# -------------------------------------------------------------
def build_slide_4(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "FEASIBILITY, RISK ANALYSIS & MITIGATION MATRIX")

    # TOP 3 FEASIBILITY CARDS (exactly matching PDF Page 4)
    feasibilities = [
        ("TECHNICAL FEASIBILITY [SUB-35ms]", [
            "• Sub-35ms query latency powered by Redis in-memory caching.",
            "• 100% cloud-native SaaS architecture; zero on-vessel sensors required.",
            "• Python FastAPI async backend with OpenAPI 3.0 specs & JWT security.",
            "• High-availability Docker deployment with 99.9% uptime SLA."
        ], COLOR_CYAN_ACCENT, 0.6),
        ("OPERATIONAL FEASIBILITY [100% BIMCO]", [
            "• 100% compliant with BIMCO GENCON 1994 & NYPE 2015 charter contracts.",
            "• Integrates official Port Trust circulars from Paradip, Haldia & Vizag.",
            "• Zero operational disruption; integrates directly into SAP/Oracle ERP.",
            "• Graceful offline fallback uses 5-year seasonal baselines during outages."
        ], COLOR_EMERALD, 4.7),
        ("ECONOMIC VIABILITY [₹28.4 Cr ROI]", [
            "• Saves ₹18.4 Cr annually on 10 MT imported coal (14.2% freight cut).",
            "• Eliminates ₹6.2 Cr in demurrage penalties ($22,500/day avoided bleed).",
            "• Saves ₹3.8 Cr through VLSFO bunker and speed route optimization.",
            "• Complete SaaS setup and licensing pays back in under 22 days."
        ], COLOR_AMBER, 8.8)
    ]

    for title, points, col, x in feasibilities:
        card = create_card(slide, x, 1.35, 3.93, 2.2, COLOR_WHITE, col, 1.2)
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.35), Inches(3.93), Inches(0.35))
        set_shape_fill(strip, col)
        strip.line.fill.background()
        p = strip.text_frame.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x+0.1), Inches(1.75), Inches(3.73), Inches(1.75))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, pt_text in enumerate(points):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = pt_text
            p.font.name = FONT_BODY
            p.font.size = Pt(7.8)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(2)

    # BOTTOM LEFT: OPERATIONAL RISKS ──► ENGINEERED MITIGATION STRATEGIES (Width: 6.8 in)
    bot_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(3.68), Inches(6.8), Inches(0.35))
    set_shape_fill(bot_banner, COLOR_NAVY_DARK)
    bot_banner.line.fill.background()
    p = bot_banner.text_frame.paragraphs[0]
    p.text = "OPERATIONAL RISKS ──► ENGINEERED MITIGATION STRATEGIES"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    risk_mitigations = [
        ("01. Red Sea Chokepoint Disruption", "Sudden Houthi strikes cause Cape diversions.",
         "01. Monte Carlo Bounds", "10,000 runs insulate against black swans.", 4.1),
        ("02. Riverine Siltation (Haldia)", "Shifting sandbars risk ship groundings.",
         "02. Astronomical Tide Models", "Hourly tide tables ensure zero grounding.", 4.82),
        ("03. Broker Feed Outage Latency", "Lag in international broker quotes.",
         "03. Redis In-Memory Cache", "Fallback to 5-yr seasonal baseline.", 5.54),
        ("04. Bay of Bengal Cyclones", "Monsoon storms degrade vessel ETA.",
         "04. Weather Speed Curves", "Copernicus ocean weather adjust speed.", 6.26)
    ]

    for r_num_title, r_desc, m_num_title, m_desc, y in risk_mitigations:
        r_card = create_card(slide, 0.6, y, 2.8, 0.65, COLOR_SLATE_BG, COLOR_RED, 1.0)
        tf_r = r_card.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = Inches(0.08)
        tf_r.margin_top = Inches(0.04)
        p1 = tf_r.paragraphs[0]
        p1.text = f"[RISK] {r_num_title}"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_RED
        p2 = tf_r.add_paragraph()
        p2.text = r_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(7)
        p2.font.color.rgb = COLOR_TEXT_MUTED

        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.45), Inches(y+0.18), Inches(0.35), Inches(0.24))
        set_shape_fill(arrow, COLOR_BLUE_PRIMARY)
        arrow.line.fill.background()

        m_card = create_card(slide, 3.85, y, 3.55, 0.65, COLOR_SLATE_BG, COLOR_EMERALD, 1.0)
        tf_m = m_card.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = Inches(0.08)
        tf_m.margin_top = Inches(0.04)
        p1 = tf_m.paragraphs[0]
        p1.text = f"[SOLVED BY] {m_num_title}"
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_EMERALD
        p2 = tf_m.add_paragraph()
        p2.text = m_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(7)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # BOTTOM RIGHT: LIVE RISK ALERTS & CONGESTION CONSOLE (Width: 5.1 in, EMBEDDED PROTOTYPE!)
    right_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.6), Inches(3.68), Inches(5.13), Inches(0.35))
    set_shape_fill(right_banner, COLOR_RED)
    right_banner.line.fill.background()
    p = right_banner.text_frame.paragraphs[0]
    p.text = "LIVE RISK ALERTS & CONGESTION CONSOLE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    create_card(slide, 7.6, 4.1, 5.13, 2.8, COLOR_WHITE, COLOR_SLATE_BORDER)
    if os.path.exists(SCREEN_RISK_CONSOLE):
        slide.shapes.add_picture(SCREEN_RISK_CONSOLE, Inches(7.7), Inches(4.18), width=Inches(4.93), height=Inches(2.45))

    p_c = slide.shapes.add_textbox(Inches(7.6), Inches(6.68), Inches(5.13), Inches(0.25))
    p = p_c.text_frame.paragraphs[0]
    p.text = "Live Prototype: Real-Time Surcharge & Weather Risk Detection in Action"
    p.font.name = FONT_BODY
    p.font.size = Pt(7.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 4)

# -------------------------------------------------------------
# SLIDE 5: IMPACT, QUANTIFIABLE ROI & ECOSYSTEM BENEFITS (MATCHING PDF PAGE 5)
# -------------------------------------------------------------
def build_slide_5(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "IMPACT, QUANTIFIABLE ROI & ECOSYSTEM BENEFITS")

    # TOP 4 METRIC CARDS (exactly matching PDF Page 5)
    metrics = [
        ("14.2% – 18.5%", "Net Freight Cost Reduction", "Timed COA commitments vs volatile spot buying", COLOR_BLUE_PRIMARY, 0.6),
        ("$15K – $30K / Day", "Demurrage Penalties Saved", "Proactive congestion alerts & idle-vessel mitigation", COLOR_RED, 3.65),
        ("100% Compliance", "Zero Dead-Freight Incurred", "Automated physical draught & berth LOA verification", COLOR_EMERALD, 6.7),
        ("11.8% Decarbonization", "IMO Carbon Intensity Reduction", "Optimized routing & parcel sizing cuts VLSFO fuel burn", COLOR_NAVY_DARK, 9.75)
    ]

    for val, label, sub, col, x in metrics:
        card = create_card(slide, x, 1.35, 2.98, 1.35, COLOR_WHITE, col, 1.5)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.08)
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(19)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(9)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_NAVY_DARK
        p2.alignment = PP_ALIGN.CENTER

        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.name = FONT_BODY
        p3.font.size = Pt(7.5)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    # MIDDLE LEFT: TARGET AUDIENCE & BENEFICIARIES (Width: 3.7 in)
    create_card(slide, 0.6, 2.85, 3.7, 4.15, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(2.85), Inches(3.7), Inches(0.35))
    set_shape_fill(ribbon_l, COLOR_NAVY_DARK)
    ribbon_l.line.fill.background()
    p = ribbon_l.text_frame.paragraphs[0]
    p.text = "TARGET AUDIENCE & BENEFICIARIES"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    audiences = [
        ("[PSU BENEFIT] Power & Steel PSUs (SAIL, NTPC)", "Locks bottom-cycle forward contracts saving ₹15–₹50+ Cr annually."),
        ("[PORT OPS] Major Port Trusts (Paradip, Haldia)", "Eliminates vessel bunching and queue delays through berth forecasting."),
        ("[DESK TOOL] Chartering & Logistics Planners", "Replaces manual Excel sheets with automated multi-corridor decision tools."),
        ("[NATIONAL] National Supply Chain Security", "Secures uninterrupted inflows of critical coking coal for steel manufacturing.")
    ]
    tb_aud = slide.shapes.add_textbox(Inches(0.72), Inches(3.25), Inches(3.46), Inches(3.6))
    tf_a = tb_aud.text_frame
    tf_a.word_wrap = True
    for i, (title, desc) in enumerate(audiences):
        p = tf_a.paragraphs[0] if i == 0 else tf_a.add_paragraph()
        p.space_after = Pt(5)
        run1 = p.add_run()
        run1.text = f"{title}\n"
        run1.font.name = FONT_HEADING
        run1.font.size = Pt(8)
        run1.font.bold = True
        run1.font.color.rgb = COLOR_NAVY_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_BODY
        run2.font.size = Pt(7.5)
        run2.font.color.rgb = COLOR_TEXT_MUTED

    # MIDDLE CENTER: MULTI-DIMENSIONAL BENEFITS (Width: 3.7 in)
    create_card(slide, 4.45, 2.85, 3.7, 4.15, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.45), Inches(2.85), Inches(3.7), Inches(0.35))
    set_shape_fill(ribbon_c, COLOR_BLUE_PRIMARY)
    ribbon_c.line.fill.background()
    p = ribbon_c.text_frame.paragraphs[0]
    p.text = "MULTI-DIMENSIONAL BENEFITS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    benefits = [
        ("[ECONOMIC] Macroeconomic Liquidity", "Lower raw material costs enhance Indian steel & power global competitiveness."),
        ("[AUDIT PROOF] Deterministic Audit Proof", "Mathematical decision logs eliminate broker asymmetry and audit scrutiny."),
        ("[ESG DECARB] Environmental Decarbonization", "Optimized routing and parcel consolidation reduce CO2 per ton-mile (IMO 2030)."),
        ("[INDIGENOUS] Maritime India 2030 Vision", "Indigenous software advances national strategic sovereignty over maritime data.")
    ]
    tb_ben = slide.shapes.add_textbox(Inches(4.57), Inches(3.25), Inches(3.46), Inches(3.6))
    tf_b = tb_ben.text_frame
    tf_b.word_wrap = True
    for i, (title, desc) in enumerate(benefits):
        p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
        p.space_after = Pt(5)
        run1 = p.add_run()
        run1.text = f"{title}\n"
        run1.font.name = FONT_HEADING
        run1.font.size = Pt(8)
        run1.font.bold = True
        run1.font.color.rgb = COLOR_BLUE_PRIMARY
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_BODY
        run2.font.size = Pt(7.5)
        run2.font.color.rgb = COLOR_TEXT_MUTED

    # MIDDLE RIGHT: LIVE CONTRACT STRATEGY & HEDGING ENGINE (Width: 4.38 in, EMBEDDED PROTOTYPE!)
    create_card(slide, 8.35, 2.85, 4.38, 4.15, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.35), Inches(2.85), Inches(4.38), Inches(0.35))
    set_shape_fill(ribbon_r, COLOR_NAVY_DARK)
    ribbon_r.line.fill.background()
    p = ribbon_r.text_frame.paragraphs[0]
    p.text = "LIVE CONTRACT STRATEGY & HEDGING ENGINE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    if os.path.exists(SCREEN_INTERLEAVER):
        slide.shapes.add_picture(SCREEN_INTERLEAVER, Inches(8.45), Inches(3.28), width=Inches(4.18), height=Inches(3.35))

    p_cr = slide.shapes.add_textbox(Inches(8.35), Inches(6.68), Inches(4.38), Inches(0.25))
    p = p_cr.text_frame.paragraphs[0]
    p.text = "Live Prototype: Simulated ₹24.8 Cr Forward Hedge Saving on Capesize Coal"
    p.font.name = FONT_BODY
    p.font.size = Pt(7.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 5)

# -------------------------------------------------------------
# SLIDE 6: RESEARCH, INDUSTRY STANDARDS & MARKET VALIDATION (MATCHING PDF PAGE 6)
# -------------------------------------------------------------
def build_slide_6(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "RESEARCH, INDUSTRY STANDARDS & MARKET VALIDATION")

    # LEFT HALF: ACADEMIC LITERATURE & MARITIME STANDARDS (Width: 5.8 in)
    create_card(slide, 0.6, 1.35, 5.8, 5.65, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(5.8), Inches(0.35))
    set_shape_fill(ribbon_l, COLOR_NAVY_DARK)
    ribbon_l.line.fill.background()
    p = ribbon_l.text_frame.paragraphs[0]
    p.text = "ACADEMIC LITERATURE & MARITIME STANDARDS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    references = [
        ("[BENCHMARK] Baltic Exchange Maritime Indices", "Daily fixture datasets for Capesize (BCI), Panamax (BPI) & Supramax (BSI) freight rates."),
        ("[ACADEMIC] Maritime Economics (Martin Stopford)", "Theoretical foundation on shipping supply/demand cycles, ton-mile elasticity & chartering."),
        ("[AI SCIENCE] Forecasting Principles (Hyndman)", "Triple Exponential Smoothing (Holt-Winters) seasonal modeling on non-stationary series."),
        ("[CONTRACTS] BIMCO Standard Charterparties", "GENCON 1994 & NYPE 2015 clauses governing laytime, demurrage, and seaworthiness."),
        ("[PORT GAZETTES] Indian Major Port Gazettes", "Official draft circulars, tidal windows & berth LOA limits from Haldia, Paradip, and Vizag.")
    ]

    tb_ref = slide.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(5.5), Inches(5.0))
    tf_r = tb_ref.text_frame
    tf_r.word_wrap = True
    for i, (title, desc) in enumerate(references):
        p = tf_r.paragraphs[0] if i == 0 else tf_r.add_paragraph()
        p.space_after = Pt(8)
        run1 = p.add_run()
        run1.text = f"{title}\n"
        run1.font.name = FONT_HEADING
        run1.font.size = Pt(8.5)
        run1.font.bold = True
        run1.font.color.rgb = COLOR_NAVY_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_BODY
        run2.font.size = Pt(8)
        run2.font.color.rgb = COLOR_TEXT_MUTED

    # RIGHT HALF: EMPIRICAL MARKET RESEARCH & PORT GROUND-TRUTH (Width: 6.13 in)
    create_card(slide, 6.6, 1.35, 6.13, 5.65, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(1.35), Inches(6.13), Inches(0.35))
    set_shape_fill(ribbon_r, COLOR_EMERALD)
    ribbon_r.line.fill.background()
    p = ribbon_r.text_frame.paragraphs[0]
    p.text = "EMPIRICAL MARKET RESEARCH & PORT GROUND-TRUTH"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Top: Two Donut Charts side-by-side with titles and legends (matching PDF Page 6!)
    # Donut 1 (Left)
    p_t1 = slide.shapes.add_textbox(Inches(6.65), Inches(1.75), Inches(2.95), Inches(0.45))
    p1 = p_t1.text_frame.paragraphs[0]
    p1.text = "Does Spot Volatility Hurt\nProcurement Margins?"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(8)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY_DARK
    p1.alignment = PP_ALIGN.CENTER

    if os.path.exists(CHART_DONUT_1):
        slide.shapes.add_picture(CHART_DONUT_1, Inches(7.2), Inches(2.2), width=Inches(1.85))

    p_leg1 = slide.shapes.add_textbox(Inches(6.65), Inches(3.75), Inches(2.95), Inches(0.35))
    p = p_leg1.text_frame.paragraphs[0]
    p.text = "▬ Agree / Impacted (94%)\n▬ Unaffected (6%)"
    p.font.name = FONT_BODY
    p.font.size = Pt(7)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # Donut 2 (Right)
    p_t2 = slide.shapes.add_textbox(Inches(9.75), Inches(1.75), Inches(2.95), Inches(0.45))
    p2 = p_t2.text_frame.paragraphs[0]
    p2.text = "Would Dynamic Draft &\nCongestion Alerts Cut Demurrage?"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(8)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_DARK
    p2.alignment = PP_ALIGN.CENTER

    if os.path.exists(CHART_DONUT_2):
        slide.shapes.add_picture(CHART_DONUT_2, Inches(10.3), Inches(2.2), width=Inches(1.85))

    p_leg2 = slide.shapes.add_textbox(Inches(9.75), Inches(3.75), Inches(2.95), Inches(0.35))
    p = p_leg2.text_frame.paragraphs[0]
    p.text = "▬ High Demand (91%)\n▬ Neutral (9%)"
    p.font.name = FONT_BODY
    p.font.size = Pt(7)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # Bottom Right: Ground-Truth Verification Live Screenshot! (matching PDF Page 6!)
    if os.path.exists(SCREEN_GROUND_TRUTH):
        slide.shapes.add_picture(SCREEN_GROUND_TRUTH, Inches(6.72), Inches(4.2), width=Inches(5.89), height=Inches(2.45))

    p_gt_cap = slide.shapes.add_textbox(Inches(6.6), Inches(6.68), Inches(6.13), Inches(0.25))
    p = p_gt_cap.text_frame.paragraphs[0]
    p.text = "Ground-Truth Verification: Real Haldia, Paradip & Vizag Draft Gazettes Integrated into Engine"
    p.font.name = FONT_BODY
    p.font.size = Pt(7.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 6)

# -------------------------------------------------------------
# SLIDE 7: LIVE PROTOTYPE SHOWCASE & PRODUCTION TECH STACK (MATCHING PDF PAGE 7)
# -------------------------------------------------------------
def build_slide_7(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "LIVE PROTOTYPE SHOWCASE & PRODUCTION TECH STACK")

    # TWO LARGE PROTOTYPE SCREENS SIDE-BY-SIDE (matching PDF Page 7!)
    # Left Screen: Module 1
    create_card(slide, 0.6, 1.35, 5.95, 3.8, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_s1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.35), Inches(5.95), Inches(0.35))
    set_shape_fill(ribbon_s1, COLOR_BLUE_PRIMARY)
    ribbon_s1.line.fill.background()
    p = ribbon_s1.text_frame.paragraphs[0]
    p.text = "MODULE 1: AI RATE FORECASTING & 90-DAY VOLATILITY CURVES"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    if os.path.exists(SCREEN_MISSION_RADAR):
        slide.shapes.add_picture(SCREEN_MISSION_RADAR, Inches(0.7), Inches(1.75), width=Inches(5.75), height=Inches(3.05))

    p_cap1 = slide.shapes.add_textbox(Inches(0.7), Inches(4.82), Inches(5.75), Inches(0.3))
    p1 = p_cap1.text_frame.paragraphs[0]
    p1.text = "Interactive 90-day Holt-Winters predictive curves across Capesize, Panamax & Supramax vessels."
    p1.font.name = FONT_BODY
    p1.font.size = Pt(7.5)
    p1.font.color.rgb = COLOR_TEXT_MUTED
    p1.alignment = PP_ALIGN.CENTER

    # Right Screen: Module 2
    create_card(slide, 6.78, 1.35, 5.95, 3.8, COLOR_WHITE, COLOR_SLATE_BORDER)
    ribbon_s2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.78), Inches(1.35), Inches(5.95), Inches(0.35))
    set_shape_fill(ribbon_s2, COLOR_EMERALD)
    ribbon_s2.line.fill.background()
    p = ribbon_s2.text_frame.paragraphs[0]
    p.text = "MODULE 2: LIVE AIS FLEET TELEMATICS & PORT CONGESTION"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    if os.path.exists(SCREEN_NEURAL_LAB):
        slide.shapes.add_picture(SCREEN_NEURAL_LAB, Inches(6.88), Inches(1.75), width=Inches(5.75), height=Inches(3.05))

    p_cap2 = slide.shapes.add_textbox(Inches(6.88), Inches(4.82), Inches(5.75), Inches(0.3))
    p2 = p_cap2.text_frame.paragraphs[0]
    p2.text = "Live AIS vessel position tracking, real-time berth draught verification & congestion monitor."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(7.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    # BOTTOM: PRODUCTION-GRADE TECHNOLOGY STACK & ARCHITECTURAL PILLARS (4 Columns, matching PDF Page 7!)
    tech_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(5.25), Inches(12.13), Inches(0.32))
    set_shape_fill(tech_banner, COLOR_NAVY_DARK)
    tech_banner.line.fill.background()
    p = tech_banner.text_frame.paragraphs[0]
    p.text = "PRODUCTION-GRADE TECHNOLOGY STACK & ARCHITECTURAL PILLARS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    tech_cols = [
        ("Frontend / GIS", ["✓ React 19 / Next.js", "✓ Tailwind CSS Design System", "✓ Chart.js Predictive Curves", "✓ Leaflet.js Dynamic GIS Map"], COLOR_CYAN_ACCENT, 0.6),
        ("Backend / API", ["✓ Python FastAPI Async", "✓ Uvicorn ASGI Server", "✓ Redis Sub-35ms Cache", "✓ PostgreSQL / PostGIS Engine"], COLOR_BLUE_PRIMARY, 3.65),
        ("AI / Math Engine", ["✓ Holt-Winters Seasonal Model", "✓ Monte Carlo 10K Simulation", "✓ UKC Astronomical Tidal Solver", "✓ Landed $/MT Linear Program"], COLOR_PURPLE, 6.7),
        ("Cloud / DevOps", ["✓ Docker Containerization", "✓ AWS EC2 / GCP Cloud Run", "✓ Automated GitHub Actions CI", "✓ 99.9% Uptime Production SLA"], COLOR_EMERALD, 9.75),
    ]

    for title, points, col, x in tech_cols:
        card = create_card(slide, x, 5.62, 2.98, 1.25, COLOR_SLATE_BG, col, 1.0)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.06)
        tf.margin_left = Inches(0.12)
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        for pt in points:
            p = tf.add_paragraph()
            p.text = pt
            p.font.name = FONT_BODY
            p.font.size = Pt(7.5)
            p.font.color.rgb = COLOR_TEXT_MAIN

    # Full Width Navy Bottom Pill (matching PDF Page 7!)
    bot_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.92), Inches(12.13), Inches(0.38))
    set_shape_fill(bot_pill, COLOR_NAVY_PILL)
    set_shape_border(bot_pill, COLOR_CYAN_ACCENT, 1.0)
    p = bot_pill.text_frame.paragraphs[0]
    p.text = "TEAM FUTURISTICS | End-to-End Functional Prototype Tested & Validated Across 6 Global Dry Bulk Corridors | SIH 2026 Final Round"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 7)

# -------------------------------------------------------------
# SLIDE 8: DETAILED TECH STACK & TEAM STRUCTURE (TEAM CREDENTIALS)
# -------------------------------------------------------------
def build_slide_8(prs):
    blank = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank)
    add_header(slide, "TECHNOLOGY STACK ARCHITECTURE & TEAM CREDENTIALS")

    # TOP: 4 TECH STACK PILLARS
    tech_categories = [
        ("Backend Core", ["FastAPI (Python 3.11+)", "Uvicorn ASGI Engine", "Redis Sub-35ms Cache", "PostgreSQL / PostGIS"], COLOR_BLUE_PRIMARY, 0.6),
        ("ML / AI & DSP", ["Holt-Winters Seasonal", "Monte Carlo 10K Engine", "ResNet-1D & CNN-LSTM", "NumPy & SciPy Signal"], COLOR_PURPLE, 3.65),
        ("Frontend & GIS", ["React 19 / Next.js", "Tailwind CSS Design", "Chart.js Visualizations", "Leaflet.js Dynamic GIS"], COLOR_CYAN_ACCENT, 6.7),
        ("DevOps & Cloud", ["Docker Containerization", "AWS EC2 / GCP Cloud Run", "GitHub Actions CI/CD", "99.9% Production SLA"], COLOR_EMERALD, 9.75)
    ]

    for cat_name, items, col, x in tech_categories:
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x+0.74), Inches(1.35), Inches(1.5), Inches(0.9))
        set_shape_fill(circle, COLOR_WHITE)
        set_shape_border(circle, col, 2.0)
        p = circle.text_frame.paragraphs[0]
        p.text = cat_name
        p.font.name = FONT_HEADING
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY_DARK
        p.alignment = PP_ALIGN.CENTER

        box = create_card(slide, x, 2.35, 2.98, 1.45, COLOR_SLATE_BG, col, 1.0)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.08)
        tf.margin_left = Inches(0.15)
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = f"☑  {item}"
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(1.5)

    # MIDDLE BANNER: TEAM STRUCTURE
    team_banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(4.0), Inches(12.13), Inches(0.35))
    set_shape_fill(team_banner, COLOR_NAVY_DARK)
    team_banner.line.fill.background()
    p = team_banner.text_frame.paragraphs[0]
    p.text = "TEAM STRUCTURE & DOMAIN EXPERTISE (TEAM FUTURISTICS)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    members = [
        ("Team Leader", "Lead Architect", "System Architect & Lead", "FastAPI, High-Speed Pipeline, Docker Deployment", COLOR_BLUE_PRIMARY, 0.6),
        ("Member 1", "AI/ML Engineer", "Time-Series & AMC Lead", "Holt-Winters, Monte Carlo, Deep Neural Models", COLOR_PURPLE, 2.65),
        ("Member 2", "GIS & Route Lead", "Maritime Route Specialist", "Bathymetry, AIS Telematics, Astronomical Tides", COLOR_CYAN_ACCENT, 4.7),
        ("Member 3", "Solvers Lead", "Optimization Engineer", "Mixed Integer Program, $/MT Landed Cost Solver", COLOR_AMBER, 6.75),
        ("Member 4", "Frontend Lead", "UI/UX & React Engineer", "React 19, Chart.js Visuals, Leaflet GIS Maps", COLOR_EMERALD, 8.8),
        ("Member 5", "DevOps & Cloud", "Reliability & QA Lead", "CI/CD, Cloud Run, API Security, SLA Testing", COLOR_NAVY_DARK, 10.85)
    ]

    for role_badge, member_name, title, domain, col, x in members:
        m_card = create_card(slide, x, 4.45, 1.88, 2.1, COLOR_WHITE, col, 1.2)
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x+0.1), Inches(4.55), Inches(1.68), Inches(0.32))
        set_shape_fill(badge, col)
        badge.line.fill.background()
        p = badge.text_frame.paragraphs[0]
        p.text = role_badge
        p.font.name = FONT_HEADING
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x+0.08), Inches(4.92), Inches(1.72), Inches(1.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = member_name
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_NAVY_DARK
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = col
        p2.alignment = PP_ALIGN.CENTER

        p3 = tf.add_paragraph()
        p3.text = domain
        p3.font.name = FONT_BODY
        p3.font.size = Pt(7)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    motto_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.65), Inches(12.13), Inches(0.42))
    set_shape_fill(motto_box, COLOR_SLATE_BG)
    set_shape_border(motto_box, COLOR_CYAN_ACCENT, 1.0)
    p = motto_box.text_frame.paragraphs[0]
    p.text = "Team Leader: Student 1 | Team Members: Student 2, Student 3, Student 4, Student 5, Student 6 | SIH 2026 Final Round"
    p.font.name = FONT_HEADING
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 8)

# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
def main():
    print("=" * 60)
    print("Generating High-Density, Zero-Whitespace SIH Presentation...")
    print("=" * 60)

    prs = Presentation()
    prs.slide_width = Inches(SLIDE_WIDTH)
    prs.slide_height = Inches(SLIDE_HEIGHT)

    print("Building Slide 1: Official Title Page...")
    build_slide_1(prs)

    print("Building Slide 2: Predictive Chartering & Route Optimizer...")
    build_slide_2(prs)

    print("Building Slide 3: Technical Approach & System Architecture...")
    build_slide_3(prs)

    print("Building Slide 4: Feasibility, Risk Analysis & Mitigation Matrix...")
    build_slide_4(prs)

    print("Building Slide 5: Impact, Quantifiable ROI & Ecosystem Benefits...")
    build_slide_5(prs)

    print("Building Slide 6: Research, Industry Standards & Market Validation...")
    build_slide_6(prs)

    print("Building Slide 7: Live Prototype Showcase & Production Tech Stack...")
    build_slide_7(prs)

    print("Building Slide 8: Technology Stack Architecture & Team Credentials...")
    build_slide_8(prs)

    output_file = "SPECTRA_SIH_2026_Presentation.pptx"
    prs.save(output_file)
    print("=" * 60)
    print(f"Presentation saved successfully to: {os.path.abspath(output_file)}")
    print(f"File size: {os.path.getsize(output_file):,} bytes")
    print("=" * 60)

if __name__ == "__main__":
    main()
