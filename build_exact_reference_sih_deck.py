import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import win32com.client

def build_reference_presentation():
    src_template = r"C:\Users\Harik\Downloads\SIH2026-IDEA-Presentation-Format.pptx"
    out_dir = r"c:\vs studio\freight-forecast"
    dst_pptx = os.path.join(out_dir, "SIH2026_FreightForecast_Pro_ExactReference_6Slides.pptx")
    dst_pdf = os.path.join(out_dir, "SIH2026_FreightForecast_Pro_ExactReference_6Slides.pdf")
    assets_dir = os.path.join(out_dir, "sih_assets")

    prs = Presentation(src_template)
    print(f"Loaded SIH template with {len(prs.slides)} slides.")

    # High-impact reference palette matching the reference deck
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_DARK_NAVY = RGBColor(15, 23, 42)       # #0F172A
    COLOR_ROYAL_BLUE = RGBColor(30, 58, 138)      # #1E3A8A - main bold titles
    COLOR_HEADING_BLUE = RGBColor(15, 76, 129)    # #0F4C81 - section headings
    COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)     # #2563EB - borders / links
    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)        # #0F172A - strong text
    COLOR_TEXT_MUTED = RGBColor(51, 65, 85)       # #334155 - body text
    COLOR_DIVIDER = RGBColor(203, 213, 225)       # #CBD5E1 - divider lines
    COLOR_ALERT_RED = RGBColor(220, 38, 38)       # #DC2626 - "Above 40% completed"
    COLOR_BOX_BG = RGBColor(239, 246, 255)        # #EFF6FF - Light container box
    COLOR_BOX_BORDER = RGBColor(147, 197, 253)    # #93C5FD

    def update_top_pill(slide, text="Team FUTURISTICS"):
        """Update or style the top-left oval/pill shape."""
        for shp in slide.shapes:
            if "Oval" in shp.name or (shp.has_text_frame and "Team Name" in shp.text):
                shp.left = Inches(0.20)
                shp.top = Inches(0.20)
                shp.width = Inches(1.85)
                shp.height = Inches(0.65)
                shp.fill.solid()
                shp.fill.fore_color.rgb = COLOR_WHITE
                shp.line.color.rgb = COLOR_ACCENT_BLUE
                shp.line.width = Pt(1.8)
                tf = shp.text_frame
                tf.clear()
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run()
                r.text = text
                r.font.name = "Arial"
                r.font.size = Pt(11)
                r.font.bold = True
                r.font.color.rgb = COLOR_ROYAL_BLUE

    def update_footer_info(slide, slide_num):
        """Ensure standard SIH footer text and slide number are crisp."""
        for shp in slide.shapes:
            if "Footer" in shp.name or (shp.has_text_frame and "@SIH" in shp.text):
                tf = shp.text_frame
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                p.text = "@SIH Idea submission- Template"
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(10)
                    r.font.color.rgb = COLOR_WHITE
            if "Slide Number" in shp.name or (shp.has_text_frame and shp.text.strip() == str(slide_num)):
                tf = shp.text_frame
                p = tf.paragraphs[0]
                p.text = str(slide_num)
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(11)
                    r.font.bold = True
                    r.font.color.rgb = COLOR_WHITE

    def clear_default_placeholders(slide):
        """Remove default instruction text boxes from the slide."""
        shapes_to_remove = []
        for shp in slide.shapes:
            if shp.name.startswith("TextBox 8") or (shp.has_text_frame and (
                "Describe your Idea" in shp.text or 
                "Technologies to be used" in shp.text or 
                "Analysis of the feasibility" in shp.text or 
                "Potential impact" in shp.text or 
                "Details / Links" in shp.text or
                "Kindly keep the maximum slides limit" in shp.text
            )):
                shapes_to_remove.append(shp)
        for shp in shapes_to_remove:
            sp = shp._element
            sp.getparent().remove(sp)

    # -------------------------------------------------------------
    # SLIDE 1: TITLE PAGE
    # -------------------------------------------------------------
    print("Building Slide 1: TITLE PAGE...")
    slide1 = prs.slides[0]
    for shp in slide1.shapes:
        if shp.name.startswith("Title") or (shp.has_text_frame and "SMART INDIA" in shp.text):
            shp.left = Inches(0.50)
            shp.top = Inches(0.50)
            shp.width = Inches(10.5)
            shp.height = Inches(0.90)
            tf = shp.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run()
            r.text = "SMART INDIA HACKATHON 2026"
            r.font.name = "Times New Roman"
            r.font.size = Pt(36)
            r.font.bold = True
            r.font.color.rgb = COLOR_ROYAL_BLUE
        elif shp.name.startswith("Subtitle") or (shp.has_text_frame and "TITLE PAGE" in shp.text):
            shp.left = Inches(0.50)
            shp.top = Inches(1.45)
            shp.width = Inches(10.5)
            shp.height = Inches(0.60)
            tf = shp.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run()
            r.text = "TITLE PAGE"
            r.font.name = "Times New Roman"
            r.font.size = Pt(26)
            r.font.bold = True
            r.font.color.rgb = COLOR_DARK_NAVY
        elif shp.has_text_frame and "Problem Statement ID" in shp.text:
            shp.left = Inches(0.60)
            shp.top = Inches(2.35)
            shp.width = Inches(6.60)
            shp.height = Inches(4.60)
            tf = shp.text_frame
            tf.clear()
            tf.word_wrap = True

            meta_items = [
                ("Problem Statement ID - ", "SIH26006 / SIH2026-LOG-01"),
                ("Problem Statement Title - ", "FreightForecast Pro: AI Freight Forecasting & Berth-Draught Vessel Routing System"),
                ("Theme - ", "Smart Logistics / Maritime & Port Supply Chain"),
                ("PS Category - ", "Software"),
                ("Team ID - ", "[As Registered on SIH Portal]"),
                ("Team Name – ", "Team FUTURISTICS")
            ]

            for idx, (label, val) in enumerate(meta_items):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p.space_before = Pt(14)
                p.space_after = Pt(2)
                
                r_dot = p.add_run()
                r_dot.text = "• "
                r_dot.font.name = "Times New Roman"
                r_dot.font.size = Pt(17)
                r_dot.font.bold = True
                r_dot.font.color.rgb = COLOR_DARK_NAVY

                r_lbl = p.add_run()
                r_lbl.text = label
                r_lbl.font.name = "Times New Roman"
                r_lbl.font.size = Pt(17)
                r_lbl.font.bold = True
                r_lbl.font.color.rgb = COLOR_DARK_NAVY

                r_val = p.add_run()
                r_val.text = val
                r_val.font.name = "Times New Roman"
                r_val.font.size = Pt(17)
                r_val.font.bold = False
                r_val.font.color.rgb = COLOR_DARK_NAVY

    # -------------------------------------------------------------
    # SLIDE 2: IDEA TITLE & 4-QUADRANT WITH CENTER DIAGRAM
    # -------------------------------------------------------------
    print("Building Slide 2: IDEA BREAKDOWN & INNOVATION...")
    slide2 = prs.slides[1]
    update_top_pill(slide2, "FUTURISTICS")
    update_footer_info(slide2, 2)
    clear_default_placeholders(slide2)

    for shp in slide2.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(1.95)
            shp.top = Inches(0.16)
            shp.width = Inches(8.40)
            shp.height = Inches(0.72)
            tf = shp.text_frame
            tf.clear()
            tf.word_wrap = True
            
            p1 = tf.paragraphs[0]
            p1.alignment = PP_ALIGN.CENTER
            r1 = p1.add_run()
            r1.text = "FreightForecast Pro: AI-Powered Maritime Bulk Freight Rate Forecasting"
            r1.font.name = "Arial"
            r1.font.size = Pt(13.5)
            r1.font.bold = True
            r1.font.italic = True
            r1.font.color.rgb = COLOR_DARK_NAVY

            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            r2 = p2.add_run()
            r2.text = "& Vessel Chartering Optimizer"
            r2.font.name = "Arial"
            r2.font.size = Pt(13.5)
            r2.font.bold = True
            r2.font.italic = True
            r2.font.color.rgb = COLOR_DARK_NAVY

    # Quadrant 1: Top Left - Problem
    tx_prob = slide2.shapes.add_textbox(Inches(0.25), Inches(0.95), Inches(5.80), Inches(1.45))
    tf_prob = tx_prob.text_frame
    tf_prob.word_wrap = True
    tf_prob.margin_left = tf_prob.margin_right = tf_prob.margin_top = tf_prob.margin_bottom = 0
    p = tf_prob.paragraphs[0]
    r = p.add_run()
    r.text = "Problem:"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE
    
    p2 = tf_prob.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = "Global ocean freight rates fluctuate by ±35% monthly due to geopolitical shocks and seasonal Bay of Bengal monsoons. India's steel and power utilities import 180M+ MT of bulk coal without forward visibility, suffering multi-million dollar budget overruns, dead-freight penalties, and $15,000–$30,000/day port demurrage fees."
    r2.font.name = "Arial"
    r2.font.size = Pt(11)
    r2.font.color.rgb = COLOR_TEXT_MAIN

    # Quadrant 2: Top Right - Our Idea
    tx_idea = slide2.shapes.add_textbox(Inches(6.35), Inches(0.95), Inches(6.65), Inches(1.45))
    tf_idea = tx_idea.text_frame
    tf_idea.word_wrap = True
    tf_idea.margin_left = tf_idea.margin_right = tf_idea.margin_top = tf_idea.margin_bottom = 0
    p = tf_idea.paragraphs[0]
    r = p.add_run()
    r.text = "Our Idea :"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE
    
    p2 = tf_idea.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = "FreightForecast Pro is an AI-powered maritime decision platform with a 3-layer approach delivering 90-day forward freight rate forecasts, dynamic tidal draught optimization, and automated spot-versus-forward hedging. It transforms fragmented Baltic fixtures, satellite AIS telemetry, and tidal circulars into actionable chartering intelligence."
    r2.font.name = "Arial"
    r2.font.size = Pt(11)
    r2.font.color.rgb = COLOR_TEXT_MAIN

    # Quadrant 3: Bottom Left - Proposed Solution
    tx_sol = slide2.shapes.add_textbox(Inches(0.25), Inches(2.55), Inches(4.35), Inches(4.35))
    tf_sol = tx_sol.text_frame
    tf_sol.word_wrap = True
    tf_sol.margin_left = tf_sol.margin_right = tf_sol.margin_top = tf_sol.margin_bottom = 0
    p = tf_sol.paragraphs[0]
    r = p.add_run()
    r.text = "Proposed Solution :"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    sol_bullets = [
        "When spot freight rates surge or seasonal disruptions strike, the system seamlessly activates a 3-layer architecture — Baltic Fixture Ingestion (primary), Satellite AIS Fleet Telematics (secondary), and Port Trust Tidal Hydrodynamics (tertiary).",
        "A smart Holt-Winters forecasting engine (α=0.28, β=0.05, γ=0.62) coupled with 10,000-run Monte Carlo simulations generates predictive rate curves with 1.7% MAPE.",
        "Dynamic Under-Keel Clearance (UKC ≥ 1.5m) solver synchronizes vessel intake with hourly astronomical tide curves to eliminate grounding risks and dead-freight penalties.",
        "Automated COA Hedging Advisor identifies cyclical market entry windows to lock 3M/12M forward fixtures at cycle-bottom rates."
    ]
    for b in sol_bullets:
        p_b = tf_sol.add_paragraph()
        p_b.space_before = Pt(7)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_ROYAL_BLUE
        r_txt = p_b.add_run()
        r_txt.text = b
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # Center Visual Mockup removed per user request
    # mockup_img = os.path.join(assets_dir, "ref_slide2_center_mockup.png")
    # if os.path.exists(mockup_img):
    #     slide2.shapes.add_picture(mockup_img, Inches(4.65), Inches(2.60), Inches(4.35), Inches(4.25))

    # Quadrant 4: Bottom Right - Innovation/Uniqueness
    tx_inn = slide2.shapes.add_textbox(Inches(9.05), Inches(2.55), Inches(4.00), Inches(4.35))
    tf_inn = tx_inn.text_frame
    tf_inn.word_wrap = True
    tf_inn.margin_left = tf_inn.margin_right = tf_inn.margin_top = tf_inn.margin_bottom = 0
    p = tf_inn.paragraphs[0]
    r = p.add_run()
    r.text = "Innovation/Uniqueness:"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    inn_bullets = [
        "India's first 3-layer maritime freight forecasting and tidal berth optimizer.",
        "Transforms raw non-standard AIS transponder pings and bathymetric gazettes into real-time anchorage demurrage risk alerts.",
        "Proprietary Market Entry Score (0–100) dynamically advising charterers when to lock forward COA fixtures before cyclical spot freight spikes.",
        "Lab-based Monte Carlo Simulation Framework lowers commercial chartering risks and trains the predictive model for real-world supply chain robustness."
    ]
    for b in inn_bullets:
        p_b = tf_inn.add_paragraph()
        p_b.space_before = Pt(8)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_ROYAL_BLUE
        r_txt = p_b.add_run()
        r_txt.text = b
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # Thin vertical divider between top sections
    div_top = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.15), Inches(0.95), Inches(0.02), Inches(1.40))
    div_top.fill.solid()
    div_top.fill.fore_color.rgb = COLOR_DIVIDER
    div_top.line.fill.background()

    # -------------------------------------------------------------
    # SLIDE 3: TECHNICAL APPROACH
    # -------------------------------------------------------------
    print("Building Slide 3: TECHNICAL APPROACH & ARCHITECTURE...")
    slide3 = prs.slides[2]
    update_top_pill(slide3, "FUTURISTICS")
    update_footer_info(slide3, 3)
    clear_default_placeholders(slide3)

    for shp in slide3.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.20)
            shp.top = Inches(0.18)
            shp.width = Inches(8.80)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "TECHNICAL APPROACH"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(24)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Left Column: Hardware & Software
    tx_tech = slide3.shapes.add_textbox(Inches(0.25), Inches(1.05), Inches(5.35), Inches(5.80))
    tf_tech = tx_tech.text_frame
    tf_tech.word_wrap = True
    tf_tech.margin_left = tf_tech.margin_right = tf_tech.margin_top = tf_tech.margin_bottom = 0
    p = tf_tech.paragraphs[0]
    r = p.add_run()
    r.text = "Hardware & Software"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_DARK_NAVY

    tech_items = [
        ("Baltic Exchange & AIS Ingestion Engine", "Primary freight rate source for Capesize (BCI), Panamax (BPI), and satellite AIS telemetry."),
        ("Holt-Winters Forecasting Engine", "Triple Exponential Smoothing (α=0.28, β=0.05, γ=0.62) with 10k Monte Carlo bounds."),
        ("SciPy Dynamic Draught Solver", "Linear programming algorithm optimizing vessel parcel intake against astronomical tide curves."),
        ("Python / NumPy / SciPy", "Simulate, validate, and benchmark maritime freight rate volatility and laytime limits."),
        ("FastAPI & Uvicorn (ASGI)", "Asynchronous high-throughput microservices architecture delivering real-time calculation endpoints."),
        ("Redis In-Memory Cache", "Sub-35 millisecond query response time for instantaneous scenario testing and live fleet lookups."),
        ("Leaflet.js & HTML5 Canvas", "Interactive nautical spatial charts with real-time vessel positions and route progress."),
        ("PostgreSQL & PostGIS", "Relational and geospatial database storing port bathymetry, berth constraints, and 5-year fixture history.")
    ]

    for title, desc in tech_items:
        p_t = tf_tech.add_paragraph()
        p_t.space_before = Pt(6)
        r_dot = p_t.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_DARK_NAVY
        
        r_tit = p_t.add_run()
        r_tit.text = f"{title}: "
        r_tit.font.name = "Arial"
        r_tit.font.size = Pt(10.5)
        r_tit.font.bold = True
        r_tit.font.color.rgb = COLOR_DARK_NAVY

        r_dsc = p_t.add_run()
        r_dsc.text = desc
        r_dsc.font.name = "Arial"
        r_dsc.font.size = Pt(10.5)
        r_dsc.font.color.rgb = COLOR_TEXT_MUTED

    # Vertical dotted divider
    div_s3 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.75), Inches(1.05), Inches(0.02), Inches(5.80))
    div_s3.fill.solid()
    div_s3.fill.fore_color.rgb = COLOR_DIVIDER
    div_s3.line.fill.background()

    # Right Area - Top: Flowchart
    tx_fc = slide3.shapes.add_textbox(Inches(5.90), Inches(1.05), Inches(3.00), Inches(0.35))
    tf_fc = tx_fc.text_frame
    tf_fc.margin_left = tf_fc.margin_right = tf_fc.margin_top = tf_fc.margin_bottom = 0
    p = tf_fc.paragraphs[0]
    r = p.add_run()
    r.text = "FLOW CHART"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.underline = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    fc_img = os.path.join(out_dir, "drawio_system_architecture.png")
    if os.path.exists(fc_img):
        slide3.shapes.add_picture(fc_img, Inches(5.90), Inches(1.40), Inches(7.15), Inches(3.45))

    # Right Area - Bottom Left: 3 LAYER APPROACH
    tx_3l = slide3.shapes.add_textbox(Inches(5.90), Inches(4.95), Inches(3.00), Inches(0.30))
    tf_3l = tx_3l.text_frame
    tf_3l.margin_left = tf_3l.margin_right = tf_3l.margin_top = tf_3l.margin_bottom = 0
    p = tf_3l.paragraphs[0]
    r = p.add_run()
    r.text = "3 LAYER APPROACH"
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.underline = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    layer_img = os.path.join(assets_dir, "ref_slide3_3layer.png")
    if os.path.exists(layer_img):
        slide3.shapes.add_picture(layer_img, Inches(5.90), Inches(5.25), Inches(3.25), Inches(1.55))

    # Right Area - Bottom Right: Container Box for GitHub, YouTube & Prototype Status
    box_git = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.30), Inches(5.00), Inches(3.75), Inches(1.80))
    box_git.fill.solid()
    box_git.fill.fore_color.rgb = COLOR_BOX_BG
    box_git.line.color.rgb = COLOR_BOX_BORDER
    box_git.line.width = Pt(1.2)

    tx_box = slide3.shapes.add_textbox(Inches(9.40), Inches(5.08), Inches(3.55), Inches(1.65))
    tf_box = tx_box.text_frame
    tf_box.word_wrap = True
    tf_box.margin_left = tf_box.margin_right = tf_box.margin_top = tf_box.margin_bottom = 0
    
    p = tf_box.paragraphs[0]
    r = p.add_run()
    r.text = "GitHub link: "
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_DARK_NAVY

    p_lnk = tf_box.add_paragraph()
    r_lnk = p_lnk.add_run()
    r_lnk.text = "https://github.com/harikesh2709-creator/FUTURISTICS"
    r_lnk.font.name = "Arial"
    r_lnk.font.size = Pt(9.5)
    r_lnk.font.bold = True
    r_lnk.font.color.rgb = COLOR_ACCENT_BLUE

    p_yt = tf_box.add_paragraph()
    p_yt.space_before = Pt(3)
    r_yt1 = p_yt.add_run()
    r_yt1.text = "YouTube video : "
    r_yt1.font.name = "Arial"
    r_yt1.font.size = Pt(12)
    r_yt1.font.bold = True
    r_yt1.font.color.rgb = COLOR_DARK_NAVY
    r_yt2 = p_yt.add_run()
    r_yt2.text = "Link"
    r_yt2.font.name = "Arial"
    r_yt2.font.size = Pt(12)
    r_yt2.font.bold = True
    r_yt2.font.color.rgb = COLOR_ACCENT_BLUE

    p_st = tf_box.add_paragraph()
    p_st.space_before = Pt(6)
    r_st = p_st.add_run()
    r_st.text = "Above 40% of the prototype is completed"
    r_st.font.name = "Arial"
    r_st.font.size = Pt(12)
    r_st.font.bold = True
    r_st.font.color.rgb = COLOR_ALERT_RED

    # -------------------------------------------------------------
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # -------------------------------------------------------------
    print("Building Slide 4: FEASIBILITY AND VIABILITY...")
    slide4 = prs.slides[3]
    update_top_pill(slide4, "FUTURISTICS")
    update_footer_info(slide4, 4)
    clear_default_placeholders(slide4)

    for shp in slide4.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.20)
            shp.top = Inches(0.18)
            shp.width = Inches(8.80)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "FEASIBILITY AND VIABILITY"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(24)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Center vertical dotted divider
    div_s4 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.50), Inches(1.05), Inches(0.02), Inches(5.80))
    div_s4.fill.solid()
    div_s4.fill.fore_color.rgb = COLOR_DIVIDER
    div_s4.line.fill.background()

    # Section 1: Top Left - Feasibility
    tx_f1 = slide4.shapes.add_textbox(Inches(0.25), Inches(1.05), Inches(6.05), Inches(2.70))
    tf_f1 = tx_f1.text_frame
    tf_f1.word_wrap = True
    tf_f1.margin_left = tf_f1.margin_right = tf_f1.margin_top = tf_f1.margin_bottom = 0
    p = tf_f1.paragraphs[0]
    r = p.add_run()
    r.text = "Feasibility"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    f1_bullets = [
        "Cloud-native SaaS simulated freight data, avoiding early physical hardware dependency on ships.",
        "Converts Baltic Exchange historical indices and AIS pings into forward freight predictions.",
        "Validation with official datasets: Ensures accurate simulation by comparing with real Baltic fixture records.",
        "Safe testing environment: Automated voyage backtesting; zero risk to maritime operations.",
        "Algorithm flexibility: Controlled seasonal decomposition allows the AI algorithm to be trained for any monsoon condition before real-time deployment."
    ]
    for b in f1_bullets:
        p_b = tf_f1.add_paragraph()
        p_b.space_before = Pt(5)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_DARK_NAVY
        r_txt = p_b.add_run()
        r_txt.text = b
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # Section 2: Top Right - Commercial feasibility
    tx_f2 = slide4.shapes.add_textbox(Inches(6.75), Inches(1.05), Inches(6.25), Inches(2.70))
    tf_f2 = tx_f2.text_frame
    tf_f2.word_wrap = True
    tf_f2.margin_left = tf_f2.margin_right = tf_f2.margin_top = tf_f2.margin_bottom = 0
    p = tf_f2.paragraphs[0]
    r = p.add_run()
    r.text = "Commercial feasibility"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    f2_bullets = [
        "Market Validation: Growing interest in maritime logistics optimization shows demand for resilient freight prediction tools.",
        "Technical Readiness: ~85% feasible using simulated freight fixtures compared with publicly available Baltic data.",
        "Timeline: 5 days prototype using stimulated freight datasets and comparison with real Baltic fixture indices.",
        "Success Likelihood: High (~90%) if simulation accurately models freight seasonality and AI reliably forecasts rate softenings."
    ]
    for b in f2_bullets:
        p_b = tf_f2.add_paragraph()
        p_b.space_before = Pt(5)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_DARK_NAVY
        r_txt = p_b.add_run()
        r_txt.text = b
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # Section 3: Bottom Left - Challenges
    tx_f3 = slide4.shapes.add_textbox(Inches(0.25), Inches(4.00), Inches(6.05), Inches(2.70))
    tf_f3 = tx_f3.text_frame
    tf_f3.word_wrap = True
    tf_f3.margin_left = tf_f3.margin_right = tf_f3.margin_top = tf_f3.margin_bottom = 0
    p = tf_f3.paragraphs[0]
    r = p.add_run()
    r.text = "Challenges"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    f3_bullets = [
        "Fast-Moving spot market rates cause frequent unpredictability and broker volatility.",
        "Commercial dry bulk shipments vary in vessel parcel size, LOA, and draft restrictions.",
        "Real-time hydrodynamic and AIS calculations consume significant server computation.",
        "Freight and AIS fixture data can be noisy or incomplete during adverse oceanic weather."
    ]
    for b in f3_bullets:
        p_b = tf_f3.add_paragraph()
        p_b.space_before = Pt(6)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_DARK_NAVY
        r_txt = p_b.add_run()
        r_txt.text = b
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # Section 4: Bottom Right - Strategy
    tx_f4 = slide4.shapes.add_textbox(Inches(6.75), Inches(4.00), Inches(6.25), Inches(2.70))
    tf_f4 = tx_f4.text_frame
    tf_f4.word_wrap = True
    tf_f4.margin_left = tf_f4.margin_right = tf_f4.margin_top = tf_f4.margin_bottom = 0
    p = tf_f4.paragraphs[0]
    r = p.add_run()
    r.text = "Strategy:"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    f4_bullets = [
        "Adaptive rate estimation and volatility compensation using Holt-Winters filtering.",
        "AI-based pattern recognition trained on open-source maritime datasets to decode market trends.",
        "Edge-optimized APIs on FastAPI, dynamic task scheduling, and sub-35ms Redis caching.",
        "Fuse Baltic indices, simulated AIS telemetry, and tidal data; implement anomaly filtering to reject corrupted data feeds."
    ]
    for b in f4_bullets:
        p_b = tf_f4.add_paragraph()
        p_b.space_before = Pt(6)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_DARK_NAVY
        r_txt = p_b.add_run()
        r_txt.text = b
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # -------------------------------------------------------------
    # SLIDE 5: IMPACT AND BENEFITS
    # -------------------------------------------------------------
    print("Building Slide 5: IMPACT AND BENEFITS...")
    slide5 = prs.slides[4]
    update_top_pill(slide5, "FUTURISTICS")
    update_footer_info(slide5, 5)
    clear_default_placeholders(slide5)

    for shp in slide5.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.20)
            shp.top = Inches(0.18)
            shp.width = Inches(8.80)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "IMPACT AND BENEFITS"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(24)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Center vertical dotted divider
    div_s5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.85), Inches(1.05), Inches(0.02), Inches(5.80))
    div_s5.fill.solid()
    div_s5.fill.fore_color.rgb = COLOR_DIVIDER
    div_s5.line.fill.background()

    # Left Column Top: Direct Impact on Target Users
    tx_imp1 = slide5.shapes.add_textbox(Inches(0.25), Inches(1.05), Inches(6.40), Inches(2.80))
    tf_imp1 = tx_imp1.text_frame
    tf_imp1.word_wrap = True
    tf_imp1.margin_left = tf_imp1.margin_right = tf_imp1.margin_top = tf_imp1.margin_bottom = 0
    p = tf_imp1.paragraphs[0]
    r = p.add_run()
    r.text = "Direct Impact on Target Users"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    imp1_bullets = [
        ("Steel Mills & Power Utilities (SAIL, Tata Steel): ", "Enables resilient coking coal procurement in volatile freight-swing environments (post-cyclone, Red Sea disruptions)."),
        ("Port Authorities (Paradip, Haldia, Vizag): ", "Provides ~30% faster vessel turnaround times, improving berth allocation in congested tidal zones."),
        ("Chartering Executives: ", "Ensures accurate rate forecasting where spot broker quotes are delayed or opaque (remote trade corridors)."),
        ("Transport & Shipping Fleets: ", "Ensures reliable, uninterrupted vessel routing even under shallow riverine draft or seasonal monsoon restrictions.")
    ]
    for lbl, desc in imp1_bullets:
        p_b = tf_imp1.add_paragraph()
        p_b.space_before = Pt(5)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_DARK_NAVY
        r_lbl = p_b.add_run()
        r_lbl.text = lbl
        r_lbl.font.name = "Arial"
        r_lbl.font.size = Pt(10.5)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = COLOR_DARK_NAVY
        r_dsc = p_b.add_run()
        r_dsc.text = desc
        r_dsc.font.name = "Arial"
        r_dsc.font.size = Pt(10.5)
        r_dsc.font.color.rgb = COLOR_TEXT_MUTED

    # Left Column Bottom: Strategic Impact
    tx_imp2 = slide5.shapes.add_textbox(Inches(0.25), Inches(4.15), Inches(6.40), Inches(2.65))
    tf_imp2 = tx_imp2.text_frame
    tf_imp2.word_wrap = True
    tf_imp2.margin_left = tf_imp2.margin_right = tf_imp2.margin_top = tf_imp2.margin_bottom = 0
    p = tf_imp2.paragraphs[0]
    r = p.add_run()
    r.text = "Strategic Impact"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    imp2_bullets = [
        "Offers broker-independent rate intelligence, highly resilient to spot volatility, dead-freight, and shipping surges.",
        "Strengthens India's maritime supply chain sovereignty, reducing foreign exchange outgo on unhedged freight.",
        "Impact: Contributes to Atmanirbhar Bharat by establishing indigenous maritime analytics capability for national logistics infrastructure."
    ]
    for b in imp2_bullets:
        p_b = tf_imp2.add_paragraph()
        p_b.space_before = Pt(6)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_DARK_NAVY
        r_txt = p_b.add_run()
        r_txt.text = b
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # Right Column Top: Economic & Strategic Benefits
    tx_eco = slide5.shapes.add_textbox(Inches(7.05), Inches(1.05), Inches(5.95), Inches(2.70))
    tf_eco = tx_eco.text_frame
    tf_eco.word_wrap = True
    tf_eco.margin_left = tf_eco.margin_right = tf_eco.margin_top = tf_eco.margin_bottom = 0
    p = tf_eco.paragraphs[0]
    r = p.add_run()
    r.text = "Economic & Strategic Benefits"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    eco_bullets = [
        "Reduces maritime shipping and chartering costs by 14.2%–18.5%, promoting indigenous logistics optimization.",
        "₹4,750 crore total addressable market by 2030 in Indian port logistics, power generation, and steel manufacturing.",
        "Superior cost effectiveness over traditional freight consultants through AI-enabled cognitive efficiency.",
        "Encourages public-private partnerships (PPP) for scalable Indian maritime technology."
    ]
    for b in eco_bullets:
        p_b = tf_eco.add_paragraph()
        p_b.space_before = Pt(6)
        r_dot = p_b.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_DARK_NAVY
        r_txt = p_b.add_run()
        r_txt.text = b
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # Right Column Bottom: Bar Chart
    chart_img = os.path.join(assets_dir, "ref_slide5_barchart.png")
    if os.path.exists(chart_img):
        slide5.shapes.add_picture(chart_img, Inches(7.30), Inches(3.95), Inches(5.45), Inches(2.85))

    # -------------------------------------------------------------
    # SLIDE 6: RESEARCH AND ANALYSIS
    # -------------------------------------------------------------
    print("Building Slide 6: RESEARCH AND ANALYSIS (6 CATEGORIES)...")
    slide6 = prs.slides[5]
    update_top_pill(slide6, "FUTURISTICS")
    update_footer_info(slide6, 6)
    clear_default_placeholders(slide6)

    for shp in slide6.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.20)
            shp.top = Inches(0.18)
            shp.width = Inches(8.80)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "Research and Analysis"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(24)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Grid of 6 Categories matching the reference slide 6:
    # Row 1: Gap & Problem Identification (Left) | Economic & Strategic Landscape (Right)
    # Row 2: Literature Survey & Competitive Analysis (Left) | Field Tests & Simulation Results (Right)
    # Row 3: Technology Benchmarking (Left) | Policy & Ecosystem Analysis (Right)

    # Dotted divider down center
    div_s6_v = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.50), Inches(1.05), Inches(0.02), Inches(5.80))
    div_s6_v.fill.solid()
    div_s6_v.fill.fore_color.rgb = COLOR_DIVIDER
    div_s6_v.line.fill.background()

    # Dotted divider row 1
    div_s6_h1 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.25), Inches(2.85), Inches(12.75), Inches(0.02))
    div_s6_h1.fill.solid()
    div_s6_h1.fill.fore_color.rgb = COLOR_DIVIDER
    div_s6_h1.line.fill.background()

    # Dotted divider row 2
    div_s6_h2 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.25), Inches(4.85), Inches(12.75), Inches(0.02))
    div_s6_h2.fill.solid()
    div_s6_h2.fill.fore_color.rgb = COLOR_DIVIDER
    div_s6_h2.line.fill.background()

    # Helper function for adding research section with link runs
    def add_research_section(slide, left, top, width, height, heading, bullet_data):
        tx = slide.shapes.add_textbox(left, top, width, height)
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = heading
        r.font.name = "Arial"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = COLOR_ROYAL_BLUE

        for text_parts in bullet_data:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(4)
            r_dot = p_b.add_run()
            r_dot.text = "• "
            r_dot.font.name = "Arial"
            r_dot.font.size = Pt(10)
            r_dot.font.bold = True
            r_dot.font.color.rgb = COLOR_DARK_NAVY

            for part_text, is_link in text_parts:
                r_txt = p_b.add_run()
                r_txt.text = part_text
                r_txt.font.name = "Arial"
                r_txt.font.size = Pt(10)
                if is_link:
                    r_txt.font.color.rgb = COLOR_ACCENT_BLUE
                    r_txt.font.underline = True
                else:
                    r_txt.font.color.rgb = COLOR_TEXT_MAIN

    # Category 1: Gap & Problem Identification (Top Left)
    c1_data = [
        [("Quote recent studies documenting the rise in ocean freight volatility and demurrage losses in Indian ports. ", False), ("link", True)],
        [("Show comparative performance of traditional unhedged spot procurement vs. AI predictive forward hedging. ", False), ("link", True)]
    ]
    add_research_section(slide6, Inches(0.25), Inches(1.05), Inches(6.05), Inches(1.70), "Gap & Problem Identification", c1_data)

    # Category 2: Economic & Strategic Landscape (Top Right)
    c2_data = [
        [("Market forecasts: cite projected growth of India’s maritime dry bulk shipping sector and expected savings from digital chartering ", False), ("1. link", True), (" ", False), ("2. link", True)]
    ]
    add_research_section(slide6, Inches(6.75), Inches(1.05), Inches(6.25), Inches(1.70), "Economic & Strategic Landscape", c2_data)

    # Category 3: Literature Survey & Competitive Analysis (Middle Left)
    c3_data = [
        [("Summarize latest global and Indian research on maritime chartering intelligence and freight indices (Baltic Dry Index, Platts, Clarksons). ", False), ("1. link", True), (" ", False), ("2. link", True), (" ", False), ("3. link", True)],
        [("Present findings from peer-reviewed experiments comparing Holt-Winters, ARIMA, and LSTM models in maritime bulk shipping. ", False), ("1. link", True), (" ", False), ("2. link", True)]
    ]
    add_research_section(slide6, Inches(0.25), Inches(2.95), Inches(6.05), Inches(1.80), "Literature Survey & Competitive Analysis", c3_data)

    # Category 4: Field Tests & Simulation Results (Middle Right)
    c4_data = [
        [("Include results from your own simulation/bench tests (e.g., 18.5% freight cost reduction, 0% grounding risk in Haldia simulation). ", False), ("link", True)],
        [("Reference international proof-of-concept studies showing automated chartering algorithms saving millions in demurrage ", False), ("link", True)]
    ]
    add_research_section(slide6, Inches(6.75), Inches(2.95), Inches(6.25), Inches(1.80), "Field Tests & Simulation Results", c4_data)

    # Category 5: Technology Benchmarking (Bottom Left)
    c5_data = [
        [("Compare accuracy, latency, and predictive horizon of traditional econometric models vs. FreightForecast Pro (e.g., 1.7% MAPE vs. 8.4% traditional error). ", False), ("link", True)],
        [("Highlight integration of AI-driven forecasting algorithms and real-time AIS spatial telemetry for demurrage avoidance. ", False), ("link", True)]
    ]
    add_research_section(slide6, Inches(0.25), Inches(4.95), Inches(6.05), Inches(1.80), "Technology Benchmarking", c5_data)

    # Category 6: Policy & Ecosystem Analysis (Bottom Right)
    c6_data = [
        [("Mention government and Ministry of Ports, Shipping and Waterways initiatives (Maritime Amrit Kaal Vision 2047, Sagarmala, PM GatiShakti alignments). ", False), ("link", True)]
    ]
    add_research_section(slide6, Inches(6.75), Inches(4.95), Inches(6.25), Inches(1.80), "Policy & Ecosystem Analysis", c6_data)

    # -------------------------------------------------------------
    # DELETE SLIDE 7 (Instructions slide) as requested by official template
    # -------------------------------------------------------------
    if len(prs.slides) > 6:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]
        print("Deleted Slide 7 (Instructions slide) to maintain pure 6-slide SIH limit.")

    prs.save(dst_pptx)
    print(f"\n[SUCCESS] Generated PowerPoint Deck: {dst_pptx}")

    # Convert to PDF using PowerPoint COM
    try:
        print("Converting PPTX to PDF via PowerPoint COM...")
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        # ppt_app.Visible = 1
        pres = ppt_app.Presentations.Open(dst_pptx, WithWindow=False)
        pres.SaveAs(dst_pdf, 32)  # 32 = ppSaveAsPDF
        
        # Also export each slide as image for visual inspection
        for i, sl in enumerate(pres.Slides):
            slide_png = os.path.join(out_dir, f"reference_style_slide_{i+1}.png")
            sl.Export(slide_png, "PNG", 1920, 1080)
            print(f"Exported Slide {i+1} screenshot: {slide_png}")
            
        pres.Close()
        ppt_app.Quit()
        print(f"[SUCCESS] Converted to High-Resolution PDF: {dst_pdf}")
    except Exception as e:
        print(f"Note on COM PDF export: {e}")

if __name__ == "__main__":
    build_reference_presentation()
