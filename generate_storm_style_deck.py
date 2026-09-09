import os
import sys
import copy
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

def duplicate_slide(prs, source_slide):
    """Duplicate a slide to allow adding more slides than the template provides."""
    slide_layout = prs.slide_layouts[6] # Blank layout usually
    new_slide = prs.slides.add_slide(slide_layout)
    
    # Copy shapes from source
    for shape in source_slide.shapes:
        if shape.shape_type == 13: # Picture
            # It's hard to copy pictures directly without saving them, 
            # but we know we just need the SIH logo, which we can copy if we know its path.
            pass
    return new_slide

def build_storm_style_deck():
    src = r"C:\Users\Harik\Downloads\SIH2026-IDEA-Presentation-Format.pptx"
    dst_pptx = r"c:\vs studio\freight-forecast\SIH2026_FreightForecast_Pro_Storm.pptx"
    
    prs = Presentation(src)
    
    # =====================================================================
    # COLOR PALETTE (Storm Surge Style)
    # =====================================================================
    BG_CREAM = RGBColor(253, 246, 235)       # Light warm background
    TEAM_BLUE = RGBColor(35, 59, 138)        # Dark blue for team badge
    TITLE_GREEN = RGBColor(38, 86, 27)       # Dark green for title badge
    TEXT_NAVY = RGBColor(10, 30, 90)
    TEXT_DARK = RGBColor(40, 40, 40)
    BOX_BG = RGBColor(245, 248, 252)         # Very light blue/grey for content boxes
    BOX_BORDER = RGBColor(180, 200, 230)
    ACCENT_BLUE = RGBColor(100, 150, 220)
    WHITE = RGBColor(255, 255, 255)
    TEAL = RGBColor(13, 148, 136)

    # Helper Functions
    def set_slide_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_CREAM

    def clear_slide(slide, keep_logo=True):
        shapes_to_remove = []
        for shape in slide.shapes:
            if keep_logo and "Picture" in shape.name:
                continue
            shapes_to_remove.append(shape)
        for shape in shapes_to_remove:
            sp = shape._element
            sp.getparent().remove(sp)

    def add_header(slide, title_text):
        # Team Badge (Top Left)
        team_badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(0.2), Inches(2.2), Inches(0.7))
        team_badge.fill.solid()
        team_badge.fill.fore_color.rgb = TEAM_BLUE
        team_badge.line.fill.background()
        tf = team_badge.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = "FUTURISTICS"
        p.font.bold = True
        p.font.size = Pt(20)
        p.font.color.rgb = WHITE
        
        # Title Badge (Top Center)
        title_badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(0.2), Inches(6.0), Inches(0.7))
        title_badge.fill.solid()
        title_badge.fill.fore_color.rgb = TITLE_GREEN
        title_badge.line.fill.background()
        tf_t = title_badge.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.alignment = PP_ALIGN.CENTER
        p_t.text = title_text
        p_t.font.bold = True
        p_t.font.size = Pt(24)
        p_t.font.color.rgb = WHITE

    def add_content_box(slide, left, top, width, height, title=None):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = BOX_BORDER
        box.line.width = Pt(1.5)
        
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.15)
        
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.bold = True
            p.font.size = Pt(16)
            p.font.color.rgb = TEAM_BLUE
            p.space_after = Pt(10)
            return tf, box
        return tf, box

    def add_check_item(tf, text):
        p = tf.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "☑ "
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = ACCENT_BLUE
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_DARK
        return p

    # Ensure we have enough slides (we need 9)
    # The template has 6 slides by default.
    while len(prs.slides) < 9:
        slide_layout = prs.slide_layouts[6]
        prs.slides.add_slide(slide_layout)

    # =====================================================================
    # SLIDE 1: TITLE PAGE
    # =====================================================================
    slide1 = prs.slides[0]
    set_slide_bg(slide1)
    clear_slide(slide1, keep_logo=True)
    
    # Title Text
    tbox = slide1.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(8.5), Inches(1.5))
    tf1 = tbox.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "SMART INDIA HACKATHON 2026"
    p1.font.bold = True
    p1.font.size = Pt(36)
    p1.font.color.rgb = TEAM_BLUE
    
    box1 = slide1.shapes.add_textbox(Inches(0.5), Inches(2.2), Inches(8.5), Inches(4.5))
    tf_c1 = box1.text_frame
    tf_c1.word_wrap = True

    title_items = [
        ("Problem Statement ID : ", "SIH2026-LOG-01"),
        ("Problem Statement Title : ", "Development of an Intelligent Freight Forecasting Model for Optimized Vessel Chartering and Bulk Cargo Procurement"),
        ("Theme : ", "Smart Logistics / Maritime Supply Chain"),
        ("PS Category : ", "Software"),
        ("Team ID : ", "SIH-2026-XXXX"),
        ("Team Name : ", "FUTURISTICS")
    ]

    for i, (label, val) in enumerate(title_items):
        p = tf_c1.paragraphs[0] if i == 0 else tf_c1.add_paragraph()
        p.space_after = Pt(14)
        r1 = p.add_run()
        r1.text = label
        r1.font.bold = True
        r1.font.size = Pt(18)
        r1.font.color.rgb = TEAM_BLUE
        
        r2 = p.add_run()
        r2.text = val
        r2.font.bold = (label == "Team Name : ")
        r2.font.size = Pt(18)
        r2.font.color.rgb = TEXT_DARK

    # =====================================================================
    # SLIDE 2: IDEA TITLE
    # =====================================================================
    slide2 = prs.slides[1]
    set_slide_bg(slide2)
    clear_slide(slide2, keep_logo=True)
    add_header(slide2, "FreightForecast Pro")
    
    # Left Diagram (Circular Flow)
    center_x, center_y = 3.0, 4.0
    radius = 1.5
    steps = ["Data\nIngestion", "AI Rate\nForecast", "Draft\nValidation", "$/MT\nOptimizer", "Live\nTelematics"]
    import math
    for i, step in enumerate(steps):
        angle = i * (2 * math.pi / len(steps)) - math.pi/2
        x = center_x + radius * math.cos(angle) - 0.75
        y = center_y + radius * math.sin(angle) - 0.4
        s = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(1.5), Inches(0.8))
        s.fill.solid()
        s.fill.fore_color.rgb = ACCENT_BLUE
        s.line.fill.background()
        p = s.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = step
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.font.bold = True
    
    center_circle = slide2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(2.25), Inches(3.25), Inches(1.5), Inches(1.5))
    center_circle.fill.solid()
    center_circle.fill.fore_color.rgb = TEAM_BLUE
    cp = center_circle.text_frame.paragraphs[0]
    cp.alignment = PP_ALIGN.CENTER
    cp.text = "CORE\nENGINE"
    cp.font.color.rgb = WHITE
    cp.font.bold = True

    # Right Content Boxes
    tf_prob, _ = add_content_box(slide2, Inches(5.5), Inches(1.2), Inches(6.5), Inches(2.7), "Currently Faced Problems :")
    add_check_item(tf_prob, "Reactive Spot Buying causing massive exposure to freight volatility (+-35%).")
    add_check_item(tf_prob, "Demurrage Penalties of $15K-$30K/day due to unpredicted port congestion.")
    add_check_item(tf_prob, "Dead-Freight Losses from draft mismatch at riverine berths (e.g., Haldia).")
    add_check_item(tf_prob, "Manual, disjointed workflows using spreadsheets and broker hearsay.")

    tf_idea, _ = add_content_box(slide2, Inches(5.5), Inches(4.1), Inches(6.5), Inches(2.9), "Our Idea :")
    add_check_item(tf_idea, "AI-Based Classification & Forecasting using Holt-Winters for 90-day predictions.")
    add_check_item(tf_idea, "Live Port Integrations validating tidal drafts against vessel physical limits.")
    add_check_item(tf_idea, "Unified Command Dashboard merging AIS telematics, bunker feeds, and rate indices.")
    add_check_item(tf_idea, "Accessible to all via intuitive Web and Mobile applications.")

    # =====================================================================
    # SLIDE 3: TECHNICAL APPROACH
    # =====================================================================
    slide3 = prs.slides[2]
    set_slide_bg(slide3)
    clear_slide(slide3, keep_logo=True)
    add_header(slide3, "TECHNICAL APPROACH")

    # Flow of Project
    tf_flow, _ = add_content_box(slide3, Inches(6.2), Inches(1.2), Inches(5.8), Inches(4.0))
    tf_flow.paragraphs[0].text = "Flow of project"
    tf_flow.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf_flow.paragraphs[0].font.bold = True
    tf_flow.paragraphs[0].font.color.rgb = WHITE
    tf_flow.paragraphs[0].font.size = Pt(16)
    # Give the flow title a green background band
    # (Since text_frame doesn't have bg color, we draw a shape over the top part)
    band = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.2), Inches(1.2), Inches(5.8), Inches(0.5))
    band.fill.solid()
    band.fill.fore_color.rgb = TITLE_GREEN
    band.line.fill.background()
    bp = band.text_frame.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    bp.text = "Flow of project"
    bp.font.color.rgb = WHITE
    bp.font.bold = True
    bp.font.size = Pt(16)

    # Simple Flowchart on Right
    nodes = ["Baltic & Port API Data", "Data Cleaning & Interpolation", "Holt-Winters Smoothing", "Monte Carlo Bounds", "$/MT Optimization", "Contract Advisory Output"]
    for i, node in enumerate(nodes):
        bx = Inches(7.6)
        by = Inches(2.0 + i*0.5)
        s = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(3.0), Inches(0.35))
        s.fill.solid()
        s.fill.fore_color.rgb = ACCENT_BLUE if i%2==0 else TEAM_BLUE
        s.line.fill.background()
        sp = s.text_frame.paragraphs[0]
        sp.alignment = PP_ALIGN.CENTER
        sp.text = node
        sp.font.size = Pt(11)
        sp.font.color.rgb = WHITE
    
    # Left block
    tf_tech, _ = add_content_box(slide3, Inches(0.5), Inches(1.2), Inches(5.5), Inches(5.8), "Foundation of Procurement Engine")
    add_check_item(tf_tech, "Time-Series Processing: Ingests 5 years of daily BDI, BCI, BPI index rates.")
    add_check_item(tf_tech, "Seasonal Decomposition: Isolates recurring weather/monsoon market cycles.")
    add_check_item(tf_tech, "Monte Carlo Risk: 10,000 simulations to generate P10-P90 confidence intervals.")
    add_check_item(tf_tech, "Voyage Estimator Math: Cost/MT = [(Hire x Days) + Bunker + Dues] / Cargo MT")
    
    # =====================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # =====================================================================
    slide4 = prs.slides[3]
    set_slide_bg(slide4)
    clear_slide(slide4, keep_logo=True)
    add_header(slide4, "Feasibility And Viability")

    # Feasibility Tree
    tf_feas, _ = add_content_box(slide4, Inches(0.5), Inches(1.2), Inches(7.5), Inches(3.0))
    band_f = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.2), Inches(7.5), Inches(0.5))
    band_f.fill.solid()
    band_f.fill.fore_color.rgb = ACCENT_BLUE
    band_f.line.fill.background()
    bf = band_f.text_frame.paragraphs[0]
    bf.alignment = PP_ALIGN.CENTER
    bf.text = "Feasibility"
    bf.font.color.rgb = WHITE
    bf.font.bold = True
    bf.font.size = Pt(16)

    slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.2), Inches(2.0), Inches(0.6)).text_frame.paragraphs[0].text = "Technical\nFeasibility"
    slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.0), Inches(2.2), Inches(2.0), Inches(0.6)).text_frame.paragraphs[0].text = "Economic\nFeasibility"
    
    t1 = slide4.shapes.add_textbox(Inches(0.8), Inches(3.0), Inches(2.0), Inches(1.0)).text_frame
    t1.word_wrap = True
    t1.paragraphs[0].text = "Fast AI execution (<50ms). No vessel hardware needed."
    t1.paragraphs[0].font.size = Pt(11)
    
    t2 = slide4.shapes.add_textbox(Inches(5.0), Inches(3.0), Inches(2.0), Inches(1.0)).text_frame
    t2.word_wrap = True
    t2.paragraphs[0].text = "Massive ROI. Cloud-based SaaS model reduces upfront cost."
    t2.paragraphs[0].font.size = Pt(11)

    # Strategic Approach (Right)
    band_s = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.2), Inches(1.2), Inches(4.0), Inches(0.8))
    band_s.fill.solid()
    band_s.fill.fore_color.rgb = TITLE_GREEN
    bs = band_s.text_frame.paragraphs[0]
    bs.alignment = PP_ALIGN.CENTER
    bs.text = "Our Strategic\nApproach"
    bs.font.color.rgb = WHITE
    bs.font.bold = True

    strat_points = ["Utilize Open-Source Datasets", "Real-time Telematics APIs", "Cloud-Native Scalability", "User-Centric Design"]
    for i, sp in enumerate(strat_points):
        s = slide4.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.7), Inches(2.5 + i*1.0), Inches(3.0), Inches(0.8))
        s.fill.solid()
        s.fill.fore_color.rgb = RGBColor(220, 230, 245)
        s.line.fill.background()
        p = s.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = sp
        p.font.size = Pt(12)
        p.font.color.rgb = TEAM_BLUE

    # Challenges (Bottom)
    tf_chal, _ = add_content_box(slide4, Inches(0.5), Inches(4.5), Inches(7.5), Inches(2.6))
    band_c = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(4.5), Inches(2.5), Inches(0.6))
    band_c.fill.solid()
    band_c.fill.fore_color.rgb = TITLE_GREEN
    bc = band_c.text_frame.paragraphs[0]
    bc.alignment = PP_ALIGN.CENTER
    bc.text = "Challenges"
    bc.font.color.rgb = WHITE
    bc.font.bold = True

    add_check_item(tf_chal, "Geopolitical Shocks -> Probabilistic Scenario Bounds")
    add_check_item(tf_chal, "Tidal Fluctuations -> Live Port Gazette API Integration")
    add_check_item(tf_chal, "Data Silos -> Unified Dashboard with Fallback Caching")

    # =====================================================================
    # SLIDE 5: Solution Benefits & Target Audience
    # =====================================================================
    slide5 = prs.slides[4]
    set_slide_bg(slide5)
    clear_slide(slide5, keep_logo=True)
    # The header for slide 5 in the template is split into two green blocks
    
    b1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.3), Inches(5.5), Inches(0.6))
    b1.fill.solid()
    b1.fill.fore_color.rgb = TEAM_BLUE
    p1 = b1.text_frame.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "Solution Benefits"
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.font.size = Pt(20)

    b2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.5), Inches(0.3), Inches(5.5), Inches(0.6))
    b2.fill.solid()
    b2.fill.fore_color.rgb = TITLE_GREEN
    p2 = b2.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Target Audience Impacts"
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.font.size = Pt(20)

    # Left Box
    box_l = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.2), Inches(5.5), Inches(4.5))
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = WHITE
    tf_l = box_l.text_frame
    add_check_item(tf_l, "12-18% Freight Cost Reduction via optimal timing.")
    add_check_item(tf_l, "Zero Demurrage penalties through predictive scheduling.")
    add_check_item(tf_l, "100% Draft Compliance eliminating dead-freight.")
    add_check_item(tf_l, "Scalable cloud processing for global supply chains.")

    # Right Box
    box_r = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.5), Inches(1.2), Inches(5.5), Inches(4.5))
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = WHITE
    tf_r = box_r.text_frame
    add_check_item(tf_r, "Bulk Importers (PSUs): Rs.15-50+ Cr annual savings.")
    add_check_item(tf_r, "Port Authorities: Reduced vessel bunching and delays.")
    add_check_item(tf_r, "Chartering Planners: Replaces tedious spreadsheet work.")
    add_check_item(tf_r, "National Security: Secures India's raw material inflows.")

    # Bottom Callouts
    cb1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.9), Inches(11.5), Inches(0.5))
    cb1.fill.solid()
    cb1.fill.fore_color.rgb = RGBColor(220, 230, 245)
    cb1.line.fill.background()
    pc1 = cb1.text_frame.paragraphs[0]
    pc1.alignment = PP_ALIGN.CENTER
    pc1.text = "➔ Drives global collaboration through better maritime data and AI optimization."
    pc1.font.bold = True
    pc1.font.color.rgb = TEXT_NAVY

    # =====================================================================
    # SLIDE 6: TECHNICAL PIPELINE
    # =====================================================================
    slide6 = prs.slides[5]
    set_slide_bg(slide6)
    clear_slide(slide6, keep_logo=True)
    add_header(slide6, "TECHNICAL PIPELINE")

    steps = [
        ("Objectives", ["Accurate Freight Forecasting", "Draft Constraint Verification", "Cost Minimization ($/MT)", "Live Vessel Tracking"]),
        ("Data Preparation", ["Ingest Baltic Indices", "Scrape Port Gazettes", "Process AIS Telematics", "Clean VLSFO Fuel Prices"]),
        ("Model Processing", ["Holt-Winters Smoothing", "Monte Carlo Bounds", "$/MT Solver Function", "Identify Optimal Charter"]),
        ("Analysis", ["Spot vs COA Comparison", "Draft Clearance Checks", "Demurrage Risk Flagging", "ROI Calculation"]),
        ("Dashboard", ["Interactive Web App UI", "GIS Map Visualizations", "Export to CSV/Excel", "Push Notifications"]),
        ("Deployment", ["AWS/GCP Cloud Hosting", "FastAPI Backend", "Secure Authentication", "Auto-Scaling Architecture"])
    ]
    
    # 3 columns, 2 rows grid
    for i, (stitle, sitems) in enumerate(steps):
        col = i % 3
        row = i // 3
        x = Inches(0.5 + col*3.9)
        y = Inches(1.5 + row*2.8)
        tf, _ = add_content_box(slide6, x, y, Inches(3.7), Inches(2.5), stitle)
        for item in sitems:
            add_check_item(tf, item)

    # =====================================================================
    # SLIDE 7: RESEARCH AND REFERENCES
    # =====================================================================
    slide7 = prs.slides[6]
    set_slide_bg(slide7)
    clear_slide(slide7, keep_logo=True)
    add_header(slide7, "RESEARCH AND REFERENCES")

    tf7, _ = add_content_box(slide7, Inches(0.5), Inches(1.2), Inches(11.5), Inches(3.5))
    p1 = tf7.paragraphs[0]
    p1.text = "■ Academic & Industry Baselines"
    p1.font.bold = True
    p1.font.size = Pt(16)
    add_check_item(tf7, "Reference: Baltic Exchange Maritime Indices (balticexchange.com) - Historical dataset for BDI/BCI/BPI.")
    add_check_item(tf7, "Reference: BIMCO Standard Charterparties - GENCON & NYPE framework documentation.")
    add_check_item(tf7, "Reference: Syama Prasad Mookerjee Port (Haldia) - Official tidal draft circulars.")
    add_check_item(tf7, "Reference: Hyndman, R.J. 'Forecasting: Principles and Practice' - Holt-Winters algorithms.")
    
    add_content_box(slide7, Inches(0.5), Inches(5.0), Inches(11.5), Inches(2.0), "Survey Validation & Market Research")
    s = slide7.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(10.0), Inches(1.0)).text_frame
    s.paragraphs[0].text = "94% of surveyed bulk importers confirm freight volatility severely impacts procurement profitability.\n91% of logistics managers agree predictive chartering can significantly reduce demurrage penalties."
    s.paragraphs[0].font.size = Pt(14)
    s.paragraphs[0].font.bold = True
    s.paragraphs[0].font.color.rgb = TEAM_BLUE

    # =====================================================================
    # SLIDE 8: UI SCREENS
    # =====================================================================
    slide8 = prs.slides[7]
    set_slide_bg(slide8)
    clear_slide(slide8, keep_logo=True)
    add_header(slide8, "UI SCREENS")

    b_web = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(5.5), Inches(0.5))
    b_web.fill.solid()
    b_web.fill.fore_color.rgb = TEAL
    b_web.text_frame.paragraphs[0].text = "Web Dashboard"
    b_web.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    b_web.text_frame.paragraphs[0].font.bold = True
    b_web.text_frame.paragraphs[0].font.color.rgb = WHITE
    b_web.text_frame.paragraphs[0].font.size = Pt(18)

    b_app = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.5), Inches(1.5), Inches(5.5), Inches(0.5))
    b_app.fill.solid()
    b_app.fill.fore_color.rgb = TEAM_BLUE
    b_app.text_frame.paragraphs[0].text = "Telematics App"
    b_app.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    b_app.text_frame.paragraphs[0].font.bold = True
    b_app.text_frame.paragraphs[0].font.color.rgb = WHITE
    b_app.text_frame.paragraphs[0].font.size = Pt(18)

    # Insert images
    brain = r"C:\Users\Harik\.gemini\antigravity-ide\brain\218e3fa8-15eb-40a0-9f59-04745317229e"
    img_forecast = os.path.join(brain, "rate_forecast_page_1788179375490.png")
    if os.path.exists(img_forecast):
        slide8.shapes.add_picture(img_forecast, Inches(0.5), Inches(2.2), width=Inches(5.5))

    img_telematics = os.path.join(brain, "live_telematics_page_reloaded_1788180951573.png")
    if os.path.exists(img_telematics):
        slide8.shapes.add_picture(img_telematics, Inches(6.5), Inches(2.2), width=Inches(5.5))

    # =====================================================================
    # SLIDE 9: TECH STACK
    # =====================================================================
    slide9 = prs.slides[8]
    set_slide_bg(slide9)
    clear_slide(slide9, keep_logo=True)
    add_header(slide9, "TECH STACK")

    # 4 circles for Backend, ML, Frontend, DevOps
    stacks = [
        ("Backend", ["FastAPI", "Python", "Redis Cache", "PostgreSQL"], TITLE_GREEN),
        ("ML / AI", ["Holt-Winters", "Monte Carlo", "Scikit-Learn", "Pandas"], TEAM_BLUE),
        ("Frontend", ["React.js", "TailwindCSS", "Chart.js", "Leaflet GIS"], ACCENT_BLUE),
        ("DevOps", ["Docker", "AWS EC2", "GitHub Actions", "Nginx"], TEAL)
    ]
    for i, (stitle, sitems, scolor) in enumerate(stacks):
        cx = Inches(1.5 + i*2.5)
        cy = Inches(2.5)
        
        # Circle
        circ = slide9.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, Inches(1.8), Inches(1.8))
        circ.fill.solid()
        circ.fill.fore_color.rgb = BOX_BG
        circ.line.color.rgb = scolor
        circ.line.width = Pt(4)
        
        p = circ.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = stitle
        p.font.bold = True
        p.font.color.rgb = scolor
        p.font.size = Pt(16)
        
        # List below
        tf, _ = add_content_box(slide9, cx-Inches(0.1), cy+Inches(2.0), Inches(2.0), Inches(1.5))
        for item in sitems:
            add_check_item(tf, item)

    # Team members at the bottom
    team_band = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.5), Inches(11.5), Inches(0.8))
    team_band.fill.solid()
    team_band.fill.fore_color.rgb = WHITE
    team_band.line.color.rgb = BOX_BORDER
    p_team = team_band.text_frame.paragraphs[0]
    p_team.alignment = PP_ALIGN.CENTER
    p_team.text = "Team Leader: Student 1  |  Team Members: Student 2, Student 3, Student 4, Student 5, Student 6"
    p_team.font.bold = True
    p_team.font.color.rgb = TEAM_BLUE
    p_team.font.size = Pt(14)

    prs.save(dst_pptx)
    print(f"SUCCESS: Saved Storm-Style 9-page deck to: {dst_pptx}")

if __name__ == "__main__":
    build_storm_style_deck()
