"""
Build SIH 2026 Infographic & Visual-Rich Reference-Style Presentation Deck for FreightForecast Pro (Team FUTURISTICS)
Strictly modeled after winning SIH decks (Team Visioncraft & Team Trinetra) and infused with real project pictures from SIH2026_FreightForecast_Pro_2:
- Slide 1: Title Page conforming to official SIH format (Times New Roman 18 pt metadata + SIH bulb logo)
- Slide 2: IDEA TITLE - Proposed Solution breakdown + System Architecture + [LIVE PROTOTYPE] Module 1 AI Forecasting Dashboard (image9.png)
- Slide 3: TECHNICAL APPROACH - Categorized Tech Stack + Process Flow Pills + [LIVE GIS PROTOTYPE] Satellite AIS Fleet Telematics Map (image10.png) + Project Links Demo Box
- Slide 4: FEASIBILITY AND VIABILITY - Feasibility, Risks, Mitigations + [LIVE RISK CONSOLE] Surcharge & Weather Risk (image5.png) + Supporting Facts Highlight Container Box
- Slide 5: IMPACT AND BENEFITS - Audience Impact + Maritime Insights + Unique Outcomes + [ROI SIMULATOR] ₹24.8 Cr Forward Hedge Chart (image6.png) + Benefits Table
- Slide 6: RESEARCH AND REFERENCES - Research Papers & Standards + Feature Comparison Matrix (with check/cross boxes) + [GROUND-TRUTH] Real Port Gazettes (image8.png) + Research Flow Chevrons
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def create_visual_reference_deck():
    src_template = r"C:\Users\Harik\Downloads\SIH2026-IDEA-Presentation-Format.pptx"
    out_dir = r"c:\vs studio\freight-forecast"
    dst_pptx = os.path.join(out_dir, "SIH2026_FreightForecast_Pro_ReferenceStyle.pptx")
    dst_pdf = os.path.join(out_dir, "SIH2026_FreightForecast_Pro_ReferenceStyle.pdf")
    img_dir = os.path.join(out_dir, "extracted_pro2_images")

    prs = Presentation(src_template)
    print(f"Loaded SIH template with {len(prs.slides)} slides.")

    # High-impact reference palette
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_DARK_NAVY = RGBColor(15, 23, 42)      # #0F172A
    COLOR_ROYAL_BLUE = RGBColor(30, 58, 138)     # #1E3A8A
    COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)    # #2563EB
    COLOR_LIGHT_BG = RGBColor(248, 250, 252)     # #F8FAFC
    COLOR_CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0
    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)       # #0F172A
    COLOR_TEXT_MUTED = RGBColor(71, 85, 105)     # #475569
    COLOR_GREEN_CHECK = RGBColor(16, 185, 129)   # #10B981
    COLOR_RED_CROSS = RGBColor(239, 68, 68)      # #EF4444
    COLOR_PEACH_BG = RGBColor(254, 243, 199)     # #FEF3C7 (Supporting facts container)
    COLOR_PEACH_BORDER = RGBColor(245, 158, 11)  # #F59E0B
    COLOR_PEACH_TEXT = RGBColor(146, 64, 14)     # #92400E
    COLOR_HEADER_BG = RGBColor(238, 242, 255)    # #EEF2FF

    def update_top_pill(slide, text="FUTURISTICS"):
        """Update or style the top-left oval/pill shape."""
        for shp in slide.shapes:
            if "Oval" in shp.name:
                shp.left = Inches(0.35)
                shp.top = Inches(0.22)
                shp.width = Inches(1.80)
                shp.height = Inches(0.68)
                shp.fill.solid()
                shp.fill.fore_color.rgb = COLOR_WHITE
                shp.line.color.rgb = COLOR_ACCENT_BLUE
                shp.line.width = Pt(2.0)
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
                    r.font.size = Pt(10)
                    r.font.bold = True
                    r.font.color.rgb = COLOR_WHITE

    def clear_default_placeholders(slide):
        """Remove default instruction text boxes from the slide."""
        shapes_to_remove = []
        for shp in slide.shapes:
            if shp.name.startswith("TextBox 8") or (shp.has_text_frame and ("Describe your Idea" in shp.text or "Technologies to be used" in shp.text or "Analysis of the feasibility" in shp.text or "Potential impact" in shp.text or "Details / Links" in shp.text)):
                shapes_to_remove.append(shp)
        for shp in shapes_to_remove:
            sp = shp._element
            sp.getparent().remove(sp)

    # -------------------------------------------------------------
    # SLIDE 1: TITLE PAGE
    # -------------------------------------------------------------
    slide1 = prs.slides[0]
    for shp in slide1.shapes:
        if shp.name.startswith("Title") or (shp.has_text_frame and "SMART INDIA" in shp.text):
            shp.left = Inches(0.40)
            shp.top = Inches(0.45)
            shp.width = Inches(10.5)
            shp.height = Inches(0.90)
            tf = shp.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = "SMART INDIA HACKATHON 2026"
            r.font.name = "Times New Roman"
            r.font.size = Pt(36)
            r.font.bold = True
            r.font.color.rgb = COLOR_ROYAL_BLUE
        elif shp.name.startswith("Subtitle") or (shp.has_text_frame and "TITLE PAGE" in shp.text):
            shp.left = Inches(0.40)
            shp.top = Inches(1.35)
            shp.width = Inches(6.50)
            shp.height = Inches(0.60)
            tf = shp.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = "TITLE PAGE"
            r.font.name = "Times New Roman"
            r.font.size = Pt(24)
            r.font.bold = True
            r.font.color.rgb = COLOR_DARK_NAVY
        elif shp.has_text_frame and "Problem Statement ID" in shp.text:
            shp.left = Inches(0.40)
            shp.top = Inches(2.20)
            shp.width = Inches(7.50)
            shp.height = Inches(4.80)
            tf = shp.text_frame
            tf.clear()
            tf.word_wrap = True

            meta_items = [
                ("Problem Statement ID –", " SIH26006"),
                ("Problem Statement Title-", " FreightForecast Pro : AI Freight Forecasting & Berth-Draught Vessel Routing System"),
                ("Theme-", " Smart Logistics / Maritime & Port Supply Chain"),
                ("PS Category-", " Software"),
                ("Team ID-", " [As Registered on SIH Portal]"),
                ("Team Name:-", " FUTURISTICS")
            ]

            for idx, (label, val) in enumerate(meta_items):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                p.space_before = Pt(13)
                p.space_after = Pt(3)
                
                r_dot = p.add_run()
                r_dot.text = "• "
                r_dot.font.name = "Times New Roman"
                r_dot.font.size = Pt(18)
                r_dot.font.bold = True
                r_dot.font.color.rgb = COLOR_DARK_NAVY

                r_lbl = p.add_run()
                r_lbl.text = label
                r_lbl.font.name = "Times New Roman"
                r_lbl.font.size = Pt(18)
                r_lbl.font.bold = True
                r_lbl.font.color.rgb = COLOR_DARK_NAVY

                r_val = p.add_run()
                r_val.text = val
                r_val.font.name = "Times New Roman"
                r_val.font.size = Pt(18)
                r_val.font.bold = False
                r_val.font.color.rgb = COLOR_DARK_NAVY

    # -------------------------------------------------------------
    # SLIDE 2: IDEA TITLE / PROPOSED SOLUTION + LIVE PROTOTYPE FORECAST CHART
    # -------------------------------------------------------------
    slide2 = prs.slides[1]
    update_top_pill(slide2, "FUTURISTICS")
    update_footer_info(slide2, 2)
    clear_default_placeholders(slide2)

    for shp in slide2.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.30)
            shp.top = Inches(0.20)
            shp.width = Inches(8.30)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "IDEA TITLE"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(26)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Left Column: Proposed Solution Breakdown
    card_l2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(1.05), Inches(6.35), Inches(5.75))
    card_l2.fill.solid()
    card_l2.fill.fore_color.rgb = COLOR_WHITE
    card_l2.line.color.rgb = COLOR_CARD_BORDER
    card_l2.line.width = Pt(1.0)

    tx_l2 = slide2.shapes.add_textbox(Inches(0.45), Inches(1.10), Inches(6.15), Inches(4.70))
    tf_l2 = tx_l2.text_frame
    tf_l2.word_wrap = True
    tf_l2.margin_left = tf_l2.margin_right = tf_l2.margin_top = tf_l2.margin_bottom = 0

    p = tf_l2.paragraphs[0]
    r = p.add_run()
    r.text = "• Proposed Solution :-"
    r.font.name = "Arial"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    p_sub = tf_l2.add_paragraph()
    p_sub.space_before = Pt(3)
    p_sub.space_after = Pt(6)
    r = p_sub.add_run()
    r.text = "A Smart Maritime Logistics Ecosystem powered by AI + Hydrodynamics + Cloud with Centralized Berth & Draught Optimization"
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = COLOR_TEXT_MAIN

    modules_s2 = [
        ("Centralized AI Freight Forecasting Hub:-", " 90-day predictive rates across Capesize (BCI), Panamax (BPI), and Supramax (BSI) using Holt-Winters seasonal decomposition with 1.7% MAPE."),
        ("Dynamic Under-Keel Clearance (UKC) Engine:-", " Hydrodynamic draught safety solver validating UKC ≥ 1.5m against astronomical tides and siltation records at Haldia, Paradip, and Vizag."),
        ("Multi-Corridor Landed Cost ($/MT) Optimizer:-", " Real-time linear program optimizing charter hire, bunker fuel (VLSFO), port dues, and canal surcharges (Suez vs Cape)."),
        ("Strategic Charterparty Hedging Advisor:-", " Automated spot market vs forward Contract of Affreightment (COA) recommendation engine, locking bottom-cycle freight rates."),
        ("Satellite AIS & Port Congestion Monitor:-", " High-frequency spatial AIS tracking vessel anchorage wait times, berth queues, and turnaround delays across Indian major ports."),
        ("Automated Demurrage Shield:-", " Early alert notification system flagging laytime risks to prevent punitive $15,000–$30,000/day shipowner demurrage claims.")
    ]

    for lbl, desc in modules_s2:
        p_mod = tf_l2.add_paragraph()
        p_mod.space_before = Pt(4)
        p_mod.space_after = Pt(1)

        r_dot = p_mod.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(10)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_ACCENT_BLUE

        r_lbl = p_mod.add_run()
        r_lbl.text = lbl
        r_lbl.font.name = "Arial"
        r_lbl.font.size = Pt(10)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = COLOR_ROYAL_BLUE

        r_desc = p_mod.add_run()
        r_desc.text = desc
        r_desc.font.name = "Arial"
        r_desc.font.size = Pt(9.5)
        r_desc.font.color.rgb = COLOR_TEXT_MAIN

    # Mathematical Formula Box at bottom left
    fn_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.45), Inches(5.95), Inches(6.15), Inches(0.75))
    fn_box.fill.solid()
    fn_box.fill.fore_color.rgb = COLOR_LIGHT_BG
    fn_box.line.color.rgb = COLOR_ACCENT_BLUE
    fn_box.line.width = Pt(1.0)
    tf = fn_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Core Mathematical Formulation & Optimization Objectives:\n"
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    r_eq = p.add_run()
    r_eq.text = "Forecast: Y(t+h) = [ℓ(t) + h·b(t)] × s(t+h-m)  |  UKC = (Chart Depth + Tide) - Arrival Draft ≥ 1.5m\nObjective: Min $/MT = [(Hire × Days) + Bunker Fuel + Port Dues] ÷ Cargo Intake MT"
    r_eq.font.name = "Arial"
    r_eq.font.size = Pt(8)
    r_eq.font.bold = False
    r_eq.font.color.rgb = COLOR_DARK_NAVY

    # Right Column: System Architecture Tiers + LIVE PROTOTYPE PICTURE (image9.png)
    card_r2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.05), Inches(6.15), Inches(5.75))
    card_r2.fill.solid()
    card_r2.fill.fore_color.rgb = COLOR_WHITE
    card_r2.line.color.rgb = COLOR_CARD_BORDER
    card_r2.line.width = Pt(1.0)

    tx_diag_title = slide2.shapes.add_textbox(Inches(6.95), Inches(1.10), Inches(5.95), Inches(0.35))
    tf_dt = tx_diag_title.text_frame
    p_dt = tf_dt.paragraphs[0]
    p_dt.alignment = PP_ALIGN.CENTER
    r = p_dt.add_run()
    r.text = "FreightForecast Pro – System Architecture & Live UI Prototype"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    user_pills = ["Steel Mills (SAIL)", "Power PSUs (NTPC)", "Port Trusts", "Chartering Desks"]
    for idx, u_txt in enumerate(user_pills):
        sh = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95 + idx * 1.50), Inches(1.48), Inches(1.42), Inches(0.32))
        sh.fill.solid()
        sh.fill.fore_color.rgb = COLOR_ROYAL_BLUE
        sh.line.color.rgb = COLOR_ROYAL_BLUE
        tf = sh.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = u_txt
        r.font.name = "Arial"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = COLOR_WHITE

    r1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95), Inches(1.88), Inches(5.95), Inches(0.34))
    r1.fill.solid()
    r1.fill.fore_color.rgb = RGBColor(254, 240, 138)
    r1.line.color.rgb = RGBColor(234, 179, 8)
    tf = r1.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "UI Presentation Layer: React 19 + Tailwind CSS + Interactive Leaflet GIS Map"
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(113, 63, 18)

    r2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.95), Inches(2.28), Inches(5.95), Inches(0.34))
    r2.fill.solid()
    r2.fill.fore_color.rgb = RGBColor(224, 231, 255)
    r2.line.color.rgb = RGBColor(99, 102, 241)
    tf = r2.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Backend & AI: FastAPI Async API (sub-35ms) ➔ Redis Cache ➔ Holt-Winters 90D Engine"
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(49, 46, 129)

    pic_hdr2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.95), Inches(2.72), Inches(5.95), Inches(0.30))
    pic_hdr2.fill.solid()
    pic_hdr2.fill.fore_color.rgb = COLOR_DARK_NAVY
    pic_hdr2.line.color.rgb = COLOR_DARK_NAVY
    tf = pic_hdr2.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "[LIVE PROTOTYPE] Module 1: AI Rate Forecasting & 90-Day Volatility Curves (MAPE 1.7%)"
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_WHITE

    img9_path = os.path.join(img_dir, "image9.png")
    if os.path.exists(img9_path):
        slide2.shapes.add_picture(img9_path, Inches(6.95), Inches(3.04), Inches(5.95), Inches(3.50))

    # -------------------------------------------------------------
    # SLIDE 3: TECHNICAL APPROACH + LIVE AIS GIS PROTOTYPE (image10.png)
    # -------------------------------------------------------------
    slide3 = prs.slides[2]
    update_top_pill(slide3, "FUTURISTICS")
    update_footer_info(slide3, 3)
    clear_default_placeholders(slide3)

    for shp in slide3.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.30)
            shp.top = Inches(0.20)
            shp.width = Inches(8.30)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "TECHNICAL APPROACH"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(26)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Left Column: Technologies, Process Flow & Project Links Box
    card_l3 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(1.05), Inches(6.15), Inches(5.75))
    card_l3.fill.solid()
    card_l3.fill.fore_color.rgb = COLOR_WHITE
    card_l3.line.color.rgb = COLOR_CARD_BORDER
    card_l3.line.width = Pt(1.0)

    tx_l3 = slide3.shapes.add_textbox(Inches(0.45), Inches(1.10), Inches(5.95), Inches(2.40))
    tf_l3 = tx_l3.text_frame
    tf_l3.word_wrap = True
    tf_l3.margin_left = tf_l3.margin_right = tf_l3.margin_top = tf_l3.margin_bottom = 0

    p = tf_l3.paragraphs[0]
    r = p.add_run()
    r.text = "• Technologies to be Used:-"
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    tech_specs = [
        ("Frontend:-", " React 19 + Next.js, TailwindCSS, Chart.js, Leaflet.js GIS"),
        ("Backend:-", " Python 3.11+, FastAPI async microservices, Uvicorn ASGI"),
        ("Databases:-", " PostgreSQL relational fixtures, PostGIS spatial, Redis cache"),
        ("AI / ML & Math:-", " Statsmodels (Holt-Winters), Scipy/Numpy (linear solver, MC 10K)"),
        ("Cloud / Infra:-", " AWS / GCP Cloud Run, Docker containers, GitHub Actions CI/CD"),
        ("Integrations:-", " Baltic API, Copernicus Marine Weather, Port Circulars, Spire AIS")
    ]

    for lbl, desc in tech_specs:
        p_t = tf_l3.add_paragraph()
        p_t.space_before = Pt(3)
        p_t.space_after = Pt(1)

        r_dot = p_t.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Arial"
        r_dot.font.size = Pt(9.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = COLOR_ACCENT_BLUE

        r_lbl = p_t.add_run()
        r_lbl.text = lbl
        r_lbl.font.name = "Arial"
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = COLOR_ROYAL_BLUE

        r_desc = p_t.add_run()
        r_desc.text = desc
        r_desc.font.name = "Arial"
        r_desc.font.size = Pt(9)
        r_desc.font.color.rgb = COLOR_TEXT_MAIN

    # Process Flow Pills
    p_pf = tf_l3.add_paragraph()
    p_pf.space_before = Pt(6)
    p_pf.space_after = Pt(2)
    r = p_pf.add_run()
    r.text = "• Process Flow :-"
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    flow_steps = [
        ("1. Ingest", "Baltic/AIS"),
        ("2. AI Model", "Holt-Winters"),
        ("3. UKC Check", "Tide/Draft"),
        ("4. Cost Solv", "Min $/MT"),
        ("5. Hedging", "Spot/COA"),
        ("6. Deploy", "API & ERP")
    ]
    f_left = 0.45
    f_top = 3.90
    f_w = 0.88
    f_h = 0.45
    for idx, (s1, s2) in enumerate(flow_steps):
        shp = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(f_left + idx * 0.98), Inches(f_top), Inches(f_w), Inches(f_h))
        shp.fill.solid()
        shp.fill.fore_color.rgb = COLOR_ROYAL_BLUE if idx % 2 == 0 else COLOR_ACCENT_BLUE
        shp.line.color.rgb = COLOR_ROYAL_BLUE
        tf = shp.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = f"{s1}\n{s2}"
        r.font.name = "Arial"
        r.font.size = Pt(7)
        r.font.bold = True
        r.font.color.rgb = COLOR_WHITE

        if idx < len(flow_steps) - 1:
            arr = slide3.shapes.add_textbox(Inches(f_left + idx * 0.98 + f_w), Inches(f_top + 0.06), Inches(0.10), Inches(0.35))
            tf_a = arr.text_frame
            tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
            p_a = tf_a.paragraphs[0]
            p_a.alignment = PP_ALIGN.CENTER
            r_a = p_a.add_run()
            r_a.text = "➔"
            r_a.font.name = "Arial"
            r_a.font.size = Pt(7.5)
            r_a.font.color.rgb = COLOR_ACCENT_BLUE

    # Boxed Card: Project Links Demo :-
    box_links = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(4.55), Inches(5.95), Inches(2.15))
    box_links.fill.solid()
    box_links.fill.fore_color.rgb = COLOR_WHITE
    box_links.line.color.rgb = COLOR_RED_CROSS
    box_links.line.width = Pt(1.5)

    tx_links = slide3.shapes.add_textbox(Inches(0.55), Inches(4.60), Inches(5.75), Inches(2.00))
    tf_lk = tx_links.text_frame
    tf_lk.word_wrap = True

    p = tf_lk.paragraphs[0]
    r = p.add_run()
    r.text = "• Project Links Demo:-"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    links_info = [
        ("• Github: ", "https://github.com/harikesh2709-creator/freight-forecast-pro", COLOR_ACCENT_BLUE),
        ("• Demo Live Prototype : ", "http://localhost:5173  (React 19 + FastAPI)", COLOR_ACCENT_BLUE),
        ("• Prototype Video Link: ", "YouTube Demo Video (2–3 mins Walkthrough)", COLOR_ACCENT_BLUE),
        ("• Product Status: ", "40% Completed (Core Engine, Live GIS, Forecasting Active)", COLOR_GREEN_CHECK)
    ]
    for lbl, val, val_col in links_info:
        p_item = tf_lk.add_paragraph()
        p_item.space_before = Pt(3)
        r1 = p_item.add_run()
        r1.text = lbl
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DARK_NAVY
        r2 = p_item.add_run()
        r2.text = val
        r2.font.name = "Arial"
        r2.font.size = Pt(9.5)
        r2.font.bold = (val_col == COLOR_GREEN_CHECK)
        r2.font.color.rgb = val_col

    # Right Column: Tech Stack Badges + LIVE SATELLITE AIS GIS PROTOTYPE (image10.png)
    card_r3 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.65), Inches(1.05), Inches(6.35), Inches(5.75))
    card_r3.fill.solid()
    card_r3.fill.fore_color.rgb = COLOR_WHITE
    card_r3.line.color.rgb = COLOR_CARD_BORDER
    card_r3.line.width = Pt(1.0)

    badge_rows = [
        ("FRONTEND", [("React 19", 0.95), ("Next.js", 0.90), ("TailwindCSS", 1.15), ("Leaflet.js", 1.05), ("Chart.js", 0.95)], Inches(1.10)),
        ("BACKEND / DB", [("Python 3.11+", 1.25), ("FastAPI Async", 1.30), ("PostgreSQL", 1.15), ("Redis Cache", 1.25)], Inches(1.68)),
        ("AI / CLOUD", [("Statsmodels", 1.10), ("Holt-Winters", 1.15), ("Monte Carlo 10K", 1.35), ("Docker", 0.85), ("AWS / GCP", 1.10)], Inches(2.26))
    ]
    for cat_title, items, top_pos in badge_rows:
        tx_t = slide3.shapes.add_textbox(Inches(6.75), top_pos, Inches(1.50), Inches(0.24))
        tf = tx_t.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = cat_title
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_ROYAL_BLUE

        c_left = 6.75
        for item_name, w_box in items:
            b_shp = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), top_pos + Inches(0.22), Inches(w_box), Inches(0.28))
            b_shp.fill.solid()
            b_shp.fill.fore_color.rgb = COLOR_LIGHT_BG
            b_shp.line.color.rgb = COLOR_ACCENT_BLUE
            b_shp.line.width = Pt(1.0)
            tf_b = b_shp.text_frame
            tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
            p_b = tf_b.paragraphs[0]
            p_b.alignment = PP_ALIGN.CENTER
            r_b = p_b.add_run()
            r_b.text = item_name
            r_b.font.name = "Arial"
            r_b.font.size = Pt(8)
            r_b.font.bold = True
            r_b.font.color.rgb = COLOR_DARK_NAVY
            c_left += w_box + 0.08

    # Frame and Picture: Module 2 Satellite AIS Fleet Telematics & Congestion GIS (image10.png)
    pic_hdr3 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.75), Inches(2.88), Inches(6.15), Inches(0.30))
    pic_hdr3.fill.solid()
    pic_hdr3.fill.fore_color.rgb = COLOR_DARK_NAVY
    pic_hdr3.line.color.rgb = COLOR_DARK_NAVY
    tf = pic_hdr3.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "[LIVE GIS PROTOTYPE] Module 2: Satellite AIS Fleet Telematics & Port Congestion Monitor"
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_WHITE

    img10_path = os.path.join(img_dir, "image10.png")
    if os.path.exists(img10_path):
        slide3.shapes.add_picture(img10_path, Inches(6.75), Inches(3.20), Inches(6.15), Inches(3.45))

    # -------------------------------------------------------------
    # SLIDE 4: FEASIBILITY AND VIABILITY + LIVE RISK CONSOLE (image5.png)
    # -------------------------------------------------------------
    slide4 = prs.slides[3]
    update_top_pill(slide4, "FUTURISTICS")
    update_footer_info(slide4, 4)
    clear_default_placeholders(slide4)

    for shp in slide4.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.30)
            shp.top = Inches(0.20)
            shp.width = Inches(8.30)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "FEASIBILITY AND VIABILITY"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(26)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Left Column: Feasibility, Challenges, Mitigations & Business Potential
    card_l4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(1.05), Inches(6.20), Inches(5.75))
    card_l4.fill.solid()
    card_l4.fill.fore_color.rgb = COLOR_WHITE
    card_l4.line.color.rgb = COLOR_CARD_BORDER
    card_l4.line.width = Pt(1.0)

    tx_l4 = slide4.shapes.add_textbox(Inches(0.45), Inches(1.10), Inches(6.00), Inches(5.60))
    tf_l4 = tx_l4.text_frame
    tf_l4.word_wrap = True
    tf_l4.margin_left = tf_l4.margin_right = tf_l4.margin_top = tf_l4.margin_bottom = 0

    p = tf_l4.paragraphs[0]
    r = p.add_run()
    r.text = "Feasibility :-"
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    feas_items = [
        ("Technical: ", "Proven AI/FastAPI/Redis stack → sub-35ms query latency; zero on-vessel sensors."),
        ("Economic: ", "Open-source cloud architecture → low cost, rapid payback in under 22 days."),
        ("Operational: ", "100% compliant with BIMCO charterparties; direct REST API for SAP/Oracle ERP."),
        ("Social: ", "Shields Indian power & steel from global freight inflation, securing energy lines.")
    ]
    for lbl, val in feas_items:
        p_item = tf_l4.add_paragraph()
        p_item.space_before = Pt(2)
        r1 = p_item.add_run()
        r1.text = "• " + lbl
        r1.font.name = "Arial"
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DARK_NAVY
        r2 = p_item.add_run()
        r2.text = val
        r2.font.name = "Arial"
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    p_ch = tf_l4.add_paragraph()
    p_ch.space_before = Pt(5)
    r = p_ch.add_run()
    r.text = "Potential Challenges:-"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    challenges = [
        "Geopolitical chokepoint blockades (Red Sea Cape diversions)",
        "Riverine siltation & shifting sandbars at ports like Haldia",
        "Freight broker quote latency & information asymmetry",
        "Cyclone weather delays across Bay of Bengal trade routes"
    ]
    for ch in challenges:
        p_item = tf_l4.add_paragraph()
        p_item.space_before = Pt(1)
        r = p_item.add_run()
        r.text = "• " + ch
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_TEXT_MAIN

    p_mit = tf_l4.add_paragraph()
    p_mit.space_before = Pt(5)
    r = p_mit.add_run()
    r.text = "Mitigation Strategies:-"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    mitigations = [
        "10,000-run Monte Carlo simulations insulate against Black Swan shock bounds",
        "Official Major Port gazettes + astronomical tide solver guarantee UKC ≥ 1.5m",
        "Redis in-memory caching with fallback to 5-year seasonal baseline datasets",
        "Copernicus ocean weather curves adjust vessel speeds and fuel consumption"
    ]
    for mit in mitigations:
        p_item = tf_l4.add_paragraph()
        p_item.space_before = Pt(1)
        r = p_item.add_run()
        r.text = "• " + mit
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_TEXT_MAIN

    p_viab = tf_l4.add_paragraph()
    p_viab.space_before = Pt(5)
    r = p_viab.add_run()
    r.text = "Viability & Business Potential:-"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    viab_items = [
        "PSU Bulk Procurement: Saves ₹18.4 Cr annually on 10 MT imported bulk coal.",
        "Demurrage Elimination: Eliminates ₹6.2 Cr in annual berth waiting penalties.",
        "Tiered B2B SaaS Subscriptions for steel mills, power PSUs & shipping agencies."
    ]
    for vb in viab_items:
        p_item = tf_l4.add_paragraph()
        p_item.space_before = Pt(1)
        r = p_item.add_run()
        r.text = "• " + vb
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_TEXT_MAIN

    # Right Column: Use Cases + LIVE RISK PICTURE (image5.png) + SUPPORTING FACTS
    card_r4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.70), Inches(1.05), Inches(6.30), Inches(5.75))
    card_r4.fill.solid()
    card_r4.fill.fore_color.rgb = COLOR_WHITE
    card_r4.line.color.rgb = COLOR_CARD_BORDER
    card_r4.line.width = Pt(1.0)

    tx_r4 = slide4.shapes.add_textbox(Inches(6.80), Inches(1.10), Inches(6.10), Inches(1.20))
    tf_r4 = tx_r4.text_frame
    tf_r4.word_wrap = True
    tf_r4.margin_left = tf_r4.margin_right = tf_r4.margin_top = tf_r4.margin_bottom = 0

    p = tf_r4.paragraphs[0]
    r = p.add_run()
    r.text = "Use Cases:-"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    use_cases = [
        ("Long-Term Charter Hedging: ", "Quantifies spot exposure vs forward COA commitments, locking bottom rates."),
        ("Draught Parcel Sizing: ", "Calculates safe cargo intake without grounding or dead-freight at Haldia/Paradip."),
        ("Demurrage Mitigation: ", "Simulates vessel queue wait times and recommends alternative discharge berths.")
    ]
    for lbl, uc in use_cases:
        p_item = tf_r4.add_paragraph()
        p_item.space_before = Pt(2)
        r1 = p_item.add_run()
        r1.text = "• " + lbl
        r1.font.name = "Arial"
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DARK_NAVY
        r2 = p_item.add_run()
        r2.text = uc
        r2.font.name = "Arial"
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    pic_hdr4 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.80), Inches(2.35), Inches(6.10), Inches(0.26))
    pic_hdr4.fill.solid()
    pic_hdr4.fill.fore_color.rgb = COLOR_DARK_NAVY
    pic_hdr4.line.color.rgb = COLOR_DARK_NAVY
    tf = pic_hdr4.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "[LIVE RISK CONSOLE] Real-Time Surcharge & Weather Risk Detection in Action"
    r.font.name = "Arial"
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = COLOR_WHITE

    img5_path = os.path.join(img_dir, "image5.png")
    if os.path.exists(img5_path):
        slide4.shapes.add_picture(img5_path, Inches(6.80), Inches(2.63), Inches(6.10), Inches(1.85))

    box_facts = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.80), Inches(4.55), Inches(6.10), Inches(2.15))
    box_facts.fill.solid()
    box_facts.fill.fore_color.rgb = COLOR_PEACH_BG
    box_facts.line.color.rgb = COLOR_PEACH_BORDER
    box_facts.line.width = Pt(1.5)

    tx_facts = slide4.shapes.add_textbox(Inches(6.88), Inches(4.60), Inches(5.95), Inches(2.05))
    tf_fc = tx_facts.text_frame
    tf_fc.word_wrap = True

    p = tf_fc.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "SUPPORTING FACTS FOR FEASIBILITY AND VIABILITY"
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = COLOR_PEACH_TEXT

    facts = [
        ("14.2% – 18.5% Net Freight Savings: ", "Backtested across 5-year Baltic Capesize fixtures for Indian coal (saves ₹18.4 Cr per 10 MT cargo)."),
        ("$15,000 – $30,000 Daily Demurrage Avoided: ", "Berth congestion forecasting eliminates idle vessel anchorage wait charges ($22.5K/day)."),
        ("Sub-35ms Edge Query Latency: ", "FastAPI async engine + Redis in-memory cache computes multi-corridor landed cost in real time."),
        ("Zero Grounding & Dead-Freight Guarantee: ", "Astronomical tidal hydrodynamics engine enforces UKC ≥ 1.5m against official Port gazettes."),
        ("Rapid 22-Day Payback Period: ", "Enterprise deployment costs are amortized within the first 3 chartered bulk shipments.")
    ]
    for lbl, fc in facts:
        p_item = tf_fc.add_paragraph()
        p_item.space_before = Pt(2)
        r1 = p_item.add_run()
        r1.text = "• " + lbl
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_PEACH_TEXT
        r2 = p_item.add_run()
        r2.text = fc
        r2.font.name = "Arial"
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_DARK_NAVY

    # -------------------------------------------------------------
    # SLIDE 5: IMPACT AND BENEFITS + LIVE HEDGING SIMULATOR (image6.png)
    # -------------------------------------------------------------
    slide5 = prs.slides[4]
    update_top_pill(slide5, "FUTURISTICS")
    update_footer_info(slide5, 5)
    clear_default_placeholders(slide5)

    for shp in slide5.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.30)
            shp.top = Inches(0.20)
            shp.width = Inches(8.30)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "IMPACT AND BENEFITS"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(26)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Top-Left: Impact on Target Audience & Maritime Insights
    card_tl5 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(1.05), Inches(4.35), Inches(3.25))
    card_tl5.fill.solid()
    card_tl5.fill.fore_color.rgb = COLOR_WHITE
    card_tl5.line.color.rgb = COLOR_CARD_BORDER
    card_tl5.line.width = Pt(1.0)

    tx_tl5 = slide5.shapes.add_textbox(Inches(0.45), Inches(1.10), Inches(4.15), Inches(3.15))
    tf_tl5 = tx_tl5.text_frame
    tf_tl5.word_wrap = True
    tf_tl5.margin_left = tf_tl5.margin_right = tf_tl5.margin_top = tf_tl5.margin_bottom = 0

    p = tf_tl5.paragraphs[0]
    r = p.add_run()
    r.text = "• Potential impact on audience:-"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    audiences = [
        ("Steel & Power PSUs (SAIL, NTPC): ", "Saves ₹15–₹50+ Cr annually by securing bottom-cycle rates."),
        ("Major Port Trusts (Paradip, Haldia): ", "Eliminates berth congestion and optimizes turnarounds."),
        ("Chartering & Procurement Desks: ", "Replaces manual Excel sheets with automated decision models."),
        ("National Maritime Economy: ", "Secures vital coking coal and raw material industrial supply chains.")
    ]
    for lbl, aud in audiences:
        p_item = tf_tl5.add_paragraph()
        p_item.space_before = Pt(2)
        r1 = p_item.add_run()
        r1.text = "• " + lbl
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DARK_NAVY
        r2 = p_item.add_run()
        r2.text = aud
        r2.font.name = "Arial"
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    p_ins = tf_tl5.add_paragraph()
    p_ins.space_before = Pt(4)
    r = p_ins.add_run()
    r.text = "• Key Maritime Logistics Insights"
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    insights = [
        "Freight represents up to 35% of landed cost for imported coal.",
        "Demurrage drains over ₹6,000 Cr annually across Indian bulk ports.",
        "85%+ of domestic chartering decisions rely on static spreadsheets."
    ]
    for ins in insights:
        p_item = tf_tl5.add_paragraph()
        p_item.space_before = Pt(1)
        r = p_item.add_run()
        r.text = "• " + ins
        r.font.name = "Arial"
        r.font.size = Pt(8)
        r.font.color.rgb = COLOR_TEXT_MUTED

    # Top-Center: Unique Outcomes from Our Solution
    card_tc5 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.85), Inches(1.05), Inches(4.25), Inches(3.25))
    card_tc5.fill.solid()
    card_tc5.fill.fore_color.rgb = COLOR_WHITE
    card_tc5.line.color.rgb = COLOR_CARD_BORDER
    card_tc5.line.width = Pt(1.0)

    tx_tc5 = slide5.shapes.add_textbox(Inches(4.95), Inches(1.10), Inches(4.05), Inches(3.15))
    tf_tc5 = tx_tc5.text_frame
    tf_tc5.word_wrap = True
    tf_tc5.margin_left = tf_tc5.margin_right = tf_tc5.margin_top = tf_tc5.margin_bottom = 0

    p = tf_tc5.paragraphs[0]
    r = p.add_run()
    r.text = "• Unique Outcomes from Solution"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    outcomes = [
        ("Freight Cost Reduction: ", "14.2% to 18.5% net freight cut via predictive charter timing and forward COA recommendations."),
        ("Demurrage Elimination: ", "Saves up to 92% of idle berth wait penalties ($15K–$30K/day avoided) through tidal synchronization."),
        ("100% Seaworthiness: ", "Zero grounding guarantee via dynamic UKC ≥ 1.5m verification against official Port gazettes."),
        ("Decarbonization (IMO 2030): ", "11.8% reduction in voyage fuel burn and GHG emissions through weather-optimized routing."),
        ("Real-Time Simulation: ", "Computes 10,000 Monte Carlo route scenarios in under 2 seconds for rapid executive decisions.")
    ]
    for lbl, oc in outcomes:
        p_item = tf_tc5.add_paragraph()
        p_item.space_before = Pt(2)
        r1 = p_item.add_run()
        r1.text = "• " + lbl
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DARK_NAVY
        r2 = p_item.add_run()
        r2.text = oc
        r2.font.name = "Arial"
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # Top-Right: LIVE HEDGING SIMULATOR PICTURE (image6.png)
    card_tr5 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.25), Inches(1.05), Inches(3.75), Inches(3.25))
    card_tr5.fill.solid()
    card_tr5.fill.fore_color.rgb = COLOR_WHITE
    card_tr5.line.color.rgb = COLOR_CARD_BORDER
    card_tr5.line.width = Pt(1.0)

    pic_hdr5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.30), Inches(1.10), Inches(3.65), Inches(0.28))
    pic_hdr5.fill.solid()
    pic_hdr5.fill.fore_color.rgb = COLOR_DARK_NAVY
    pic_hdr5.line.color.rgb = COLOR_DARK_NAVY
    tf = pic_hdr5.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "[ROI SIMULATOR] ₹24.8 Cr Forward Hedge Saving"
    r.font.name = "Arial"
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = COLOR_WHITE

    img6_path = os.path.join(img_dir, "image6.png")
    if os.path.exists(img6_path):
        slide5.shapes.add_picture(img6_path, Inches(9.30), Inches(1.42), Inches(3.65), Inches(2.80))

    # Bottom Half: Full-Width Table: Benefits of the Solution
    p_tbl_hdr = slide5.shapes.add_textbox(Inches(0.35), Inches(4.38), Inches(12.65), Inches(0.30))
    tf_th = p_tbl_hdr.text_frame
    p = tf_th.paragraphs[0]
    r = p.add_run()
    r.text = "• Benefits of the Solution (Social, Economic, Environmental)"
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    tbl_shape = slide5.shapes.add_table(4, 3, Inches(0.35), Inches(4.70), Inches(12.65), Inches(2.15))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.20)
    tbl.columns[1].width = Inches(4.75)
    tbl.columns[2].width = Inches(5.70)

    headers = ["Type", "Benefit", "Supporting Example / Measurable Metric"]
    for c_idx, h_txt in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_HEADER_BG
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h_txt
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = COLOR_ROYAL_BLUE

    table_data = [
        ("Social & Strategic", "National Supply Chain Security & Energy Price Stability", "Shields Indian power tariffs and infrastructure steel from global shipping volatility; guarantees uninterrupted coking coal inflows."),
        ("Economic", "₹28.4 Cr Annual Cost Savings per 10 MT Imported Cargo", "Saves ₹18.4 Cr via predictive freight timing (14.2% cut), ₹6.2 Cr via demurrage elimination, and ₹3.8 Cr through bunker fuel speed curves."),
        ("Environmental", "11.8% Maritime Carbon Intensity Reduction (IMO 2030)", "Hydrodynamic route & parcel optimization reduces VLSFO bunker fuel burn; aligns with IMO Carbon Intensity Indicator (CII) targets.")
    ]

    for r_idx, (c0, c1, c2) in enumerate(table_data, 1):
        cell0 = tbl.cell(r_idx, 0)
        cell0.fill.solid()
        cell0.fill.fore_color.rgb = COLOR_WHITE
        cell0.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell0.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = c0
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_ROYAL_BLUE

        cell1 = tbl.cell(r_idx, 1)
        cell1.fill.solid()
        cell1.fill.fore_color.rgb = COLOR_WHITE
        cell1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell1.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = c1
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = COLOR_DARK_NAVY

        cell2 = tbl.cell(r_idx, 2)
        cell2.fill.solid()
        cell2.fill.fore_color.rgb = COLOR_WHITE
        cell2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell2.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = c2
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_TEXT_MAIN

    # -------------------------------------------------------------
    # SLIDE 6: RESEARCH AND REFERENCES + REAL PORT GAZETTES (image8.png)
    # -------------------------------------------------------------
    slide6 = prs.slides[5]
    update_top_pill(slide6, "FUTURISTICS")
    update_footer_info(slide6, 6)
    clear_default_placeholders(slide6)

    for shp in slide6.shapes:
        if shp.name.startswith("Title"):
            shp.left = Inches(2.30)
            shp.top = Inches(0.20)
            shp.width = Inches(8.30)
            shp.height = Inches(0.70)
            tf = shp.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = "RESEARCH AND REFERENCES"
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(26)
                r.font.bold = True
                r.font.color.rgb = COLOR_DARK_NAVY

    # Left Column: Research Papers, Standards & Project Demo Links
    card_l6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(1.05), Inches(4.15), Inches(4.55))
    card_l6.fill.solid()
    card_l6.fill.fore_color.rgb = COLOR_WHITE
    card_l6.line.color.rgb = COLOR_CARD_BORDER
    card_l6.line.width = Pt(1.0)

    tx_l6 = slide6.shapes.add_textbox(Inches(0.45), Inches(1.10), Inches(3.95), Inches(3.20))
    tf_l6 = tx_l6.text_frame
    tf_l6.word_wrap = True
    tf_l6.margin_left = tf_l6.margin_right = tf_l6.margin_top = tf_l6.margin_bottom = 0

    p = tf_l6.paragraphs[0]
    r = p.add_run()
    r.text = "• Research Papers:-"
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    papers = [
        ("a. Stopford, M., ", "“Maritime Economics (3rd Ed),” Routledge. Shipping freight cycles, market balance & ton-mile elasticity."),
        ("b. Hyndman, R.J., ", "“Forecasting: Principles & Practice,” OTexts. Multi-seasonal Holt-Winters on freight indices."),
        ("c. Alizadeh, A.H., ", "“Investment Strategies in Shipping,” Palgrave. FFA & spot hedging models.")
    ]
    for lbl, desc in papers:
        p_p = tf_l6.add_paragraph()
        p_p.space_before = Pt(2)
        r1 = p_p.add_run()
        r1.text = lbl
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DARK_NAVY
        r2 = p_p.add_run()
        r2.text = desc
        r2.font.name = "Arial"
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    p_std = tf_l6.add_paragraph()
    p_std.space_before = Pt(4)
    r = p_std.add_run()
    r.text = "• Maritime Standards & Circulars:-"
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    standards = [
        ("a. BIMCO Standard Contracts: ", "GENCON 1994 (Voyage) & NYPE 2015."),
        ("b. Ministry of Shipping: ", "Maritime India Vision 2030 Policy Framework."),
        ("c. Indian Port Authorities: ", "Draft Circulars (Paradip, Haldia, Vizag).")
    ]
    for lbl, desc in standards:
        p_s = tf_l6.add_paragraph()
        p_s.space_before = Pt(1)
        r1 = p_s.add_run()
        r1.text = lbl
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DARK_NAVY
        r2 = p_s.add_run()
        r2.text = desc
        r2.font.name = "Arial"
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_TEXT_MAIN

    # Boxed Card: Project Links Demo :-
    box_l6_links = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(4.35), Inches(3.95), Inches(1.15))
    box_l6_links.fill.solid()
    box_l6_links.fill.fore_color.rgb = COLOR_WHITE
    box_l6_links.line.color.rgb = COLOR_RED_CROSS
    box_l6_links.line.width = Pt(1.5)

    tx_l6_lk = slide6.shapes.add_textbox(Inches(0.52), Inches(4.38), Inches(3.80), Inches(1.05))
    tf_l6k = tx_l6_lk.text_frame
    tf_l6k.word_wrap = True

    p = tf_l6k.paragraphs[0]
    r = p.add_run()
    r.text = "• Project Links Demo:-"
    r.font.name = "Arial"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    p_g = tf_l6k.add_paragraph()
    p_g.space_before = Pt(1)
    r1 = p_g.add_run()
    r1.text = "• Github: "
    r1.font.name = "Arial"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK_NAVY
    r2 = p_g.add_run()
    r2.text = "https://github.com/.../freight-forecast-pro"
    r2.font.name = "Arial"
    r2.font.size = Pt(8)
    r2.font.color.rgb = COLOR_ACCENT_BLUE

    p_d = tf_l6k.add_paragraph()
    p_d.space_before = Pt(1)
    r1 = p_d.add_run()
    r1.text = "• Demo Prototype: "
    r1.font.name = "Arial"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK_NAVY
    r2 = p_d.add_run()
    r2.text = "http://localhost:5173"
    r2.font.name = "Arial"
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = COLOR_ACCENT_BLUE

    # Center: Feature Comparison Matrix Table
    comp_tbl_shape = slide6.shapes.add_table(9, 4, Inches(4.60), Inches(1.05), Inches(5.15), Inches(4.55))
    c_tbl = comp_tbl_shape.table
    c_tbl.columns[0].width = Inches(2.30)
    c_tbl.columns[1].width = Inches(0.90)
    c_tbl.columns[2].width = Inches(0.90)
    c_tbl.columns[3].width = Inches(1.05)

    c_headers = ["Feature", "Manual Excel", "S&P Platts", "FreightForecast\nPro"]
    for idx, h_txt in enumerate(c_headers):
        cell = c_tbl.cell(0, idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_HEADER_BG
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h_txt
        r.font.name = "Arial"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = COLOR_ROYAL_BLUE

    matrix_rows = [
        ("1. 90-Day Predictive Rate Forecast", False, False, True),
        ("2. Dynamic Tidal UKC Hydrodynamics", False, False, True),
        ("3. Landed Cost ($/MT) Multi-Corridor Solver", False, False, True),
        ("4. Spot vs COA Contract Hedging Advisor", False, False, True),
        ("5. Real-Time Satellite AIS Vessel Tracking", False, True, True),
        ("6. Demurrage Risk & Laytime Calculator", False, False, True),
        ("7. Indian Major Port Gazette Integration", False, False, True),
        ("8. Enterprise ERP Integration (SAP/Oracle)", False, False, True)
    ]

    for r_idx, (f_name, has_excel, has_platts, has_our) in enumerate(matrix_rows, 1):
        cell0 = c_tbl.cell(r_idx, 0)
        cell0.fill.solid()
        cell0.fill.fore_color.rgb = COLOR_WHITE
        cell0.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell0.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = f_name
        r.font.name = "Arial"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = COLOR_DARK_NAVY

        for c_idx, val in enumerate([has_excel, has_platts, has_our], 1):
            cell = c_tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(209, 250, 229) if val else RGBColor(254, 226, 226)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run()
            r.text = "[✔]" if val else "[✖]"
            r.font.name = "Arial"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(5, 150, 105) if val else RGBColor(220, 38, 38)

    # Right Column: Ground-Truth Port Gazettes Picture (image8.png)
    card_tr6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.85), Inches(1.05), Inches(3.15), Inches(4.55))
    card_tr6.fill.solid()
    card_tr6.fill.fore_color.rgb = COLOR_WHITE
    card_tr6.line.color.rgb = COLOR_CARD_BORDER
    card_tr6.line.width = Pt(1.0)

    pic_hdr6 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.90), Inches(1.10), Inches(3.05), Inches(0.36))
    pic_hdr6.fill.solid()
    pic_hdr6.fill.fore_color.rgb = COLOR_DARK_NAVY
    pic_hdr6.line.color.rgb = COLOR_DARK_NAVY
    tf = pic_hdr6.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "[GROUND-TRUTH] Port Circulars\nHaldia, Paradip & Vizag Drafts"
    r.font.name = "Arial"
    r.font.size = Pt(7.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_WHITE

    img8_path = os.path.join(img_dir, "image8.png")
    if os.path.exists(img8_path):
        slide6.shapes.add_picture(img8_path, Inches(9.90), Inches(1.50), Inches(3.05), Inches(4.00))

    # Bottom Half: Horizontal Research Flow Chevrons
    tx_rf = slide6.shapes.add_textbox(Inches(0.35), Inches(5.68), Inches(12.65), Inches(0.28))
    tf_rf = tx_rf.text_frame
    p = tf_rf.paragraphs[0]
    r = p.add_run()
    r.text = "• Research Flow :-"
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = COLOR_ROYAL_BLUE

    res_flow_steps = [
        "Problem\nIdentification",
        "Literature &\nMarket Study",
        "Gap\nAnalysis",
        "Technology\nExploration",
        "Hydrodynamic\nModeling",
        "Validation &\nFeasibility",
        "Proposed\nSolution Design",
        "FreightForecast\nEcosystem"
    ]
    rf_left = 0.35
    rf_top = 5.98
    rf_w = 1.52
    rf_h = 0.55
    for idx, step_txt in enumerate(res_flow_steps):
        shp = slide6.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(rf_left + idx * 1.57), Inches(rf_top), Inches(rf_w), Inches(rf_h))
        shp.fill.solid()
        shp.fill.fore_color.rgb = COLOR_ROYAL_BLUE if idx in [0, 6, 7] else COLOR_ACCENT_BLUE
        shp.line.color.rgb = COLOR_WHITE
        shp.line.width = Pt(1.0)
        tf = shp.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = step_txt
        r.font.name = "Arial"
        r.font.size = Pt(7)
        r.font.bold = True
        r.font.color.rgb = COLOR_WHITE

    # Remove Slide 7 (Instructions slide) so it is a pristine 6-slide submission presentation
    if len(prs.slides) > 6:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]
        print("Removed Slide 7 guidelines. Presentation is now exactly 6 slides.")

    prs.save(dst_pptx)
    print(f"Successfully saved Visual Reference-Style PPTX to: {dst_pptx}")

if __name__ == "__main__":
    create_visual_reference_deck()
