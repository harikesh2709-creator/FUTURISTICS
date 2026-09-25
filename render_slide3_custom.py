import asyncio
from playwright.async_api import async_playwright
import os

HTML_SLIDE_3_CUSTOM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; width: 1400px; height: 650px; overflow: hidden; }
        .wrapper { display: flex; flex-direction: column; padding: 20px; width: 100%; height: 100%; box-sizing: border-box; }
        
        .section-title { font-size: 26px; font-weight: 900; color: #1e3a8a; margin-bottom: 20px; text-transform: uppercase; text-decoration: underline; text-underline-offset: 6px; }
        
        /* Top Section: Flowchart */
        .top-section { height: 350px; border: 2px dashed #cbd5e1; border-radius: 15px; padding: 20px; display: flex; align-items: center; justify-content: center; position: relative; background: #f8fafc; margin-bottom: 25px; }
        
        .flow-container { display: flex; width: 100%; justify-content: space-between; align-items: center; position: relative; }
        
        .flow-col { display: flex; flex-direction: column; gap: 25px; z-index: 2; width: 30%; }
        
        .box { padding: 18px; border-radius: 10px; font-weight: 700; font-size: 16px; text-align: center; color: white; box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
        .box-red { background: linear-gradient(135deg, #ef4444, #b91c1c); }
        .box-blue { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
        .box-green { background: linear-gradient(135deg, #10b981, #047857); }
        .box-purple { background: linear-gradient(135deg, #8b5cf6, #5b21b6); }
        
        .large-box { width: 38%; padding: 25px; border-radius: 15px; background: linear-gradient(135deg, #cffafe, #a5f3fc); border: 3px solid #06b6d4; text-align: center; z-index: 2; box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .lb-title { color: #083344; font-weight: 900; font-size: 20px; margin-bottom: 15px; }
        .lb-item { background: white; padding: 10px; border-radius: 6px; color: #155e75; font-weight: 700; margin-bottom: 10px; font-size: 15px; border: 1px solid #67e8f9; }
        
        /* Arrows (pseudo-elements or simple lines using SVGs) */
        .arrow-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }
        
        /* Bottom Section */
        .bottom-section { display: flex; height: 215px; gap: 25px; }
        
        /* Bottom Left: 3 Layer Approach */
        .bottom-left { flex: 1; position: relative; padding-top: 10px; }
        .layer { position: absolute; width: 320px; height: 80px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; color: white; box-shadow: 0 8px 20px rgba(0,0,0,0.15); transition: all 0.3s ease; }
        .layer-1 { top: 90px; left: 20px; background: #0f172a; border: 2px solid #38bdf8; z-index: 3; }
        .layer-2 { top: 50px; left: 60px; background: #b91c1c; border: 2px solid #f87171; z-index: 2; }
        .layer-3 { top: 10px; left: 100px; background: #047857; border: 2px solid #34d399; z-index: 1; }
        
        /* Labels pointing to layers */
        .layer-label { position: absolute; font-weight: 800; font-size: 15px; color: #1e293b; background: white; padding: 6px 12px; border: 2px solid #cbd5e1; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .ll-1 { top: 115px; left: 380px; }
        .ll-2 { top: 65px; left: 420px; }
        .ll-3 { top: 15px; left: 460px; }
        
        /* Bottom Right: Links */
        .bottom-right { flex: 1; background: #bfdbfe; border-radius: 12px; padding: 25px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 8px 15px rgba(0,0,0,0.05); border: 2px solid #93c5fd; }
        .link-row { font-size: 22px; font-weight: 800; color: #1e3a8a; margin-bottom: 15px; }
        .link-url { color: #2563eb; text-decoration: underline; word-break: break-all; }
        .link-url-yt { color: #db2777; text-decoration: underline; }
        .status-row { font-size: 26px; font-weight: 900; color: #dc2626; margin-top: 15px; }
        
    </style>
</head>
<body>
<div class="wrapper">
    
    <div class="section-title">FLOW CHART</div>
    <div class="top-section">
        
        <!-- SVG for Arrows -->
        <svg class="arrow-svg" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#64748b" />
                </marker>
            </defs>
            <!-- Ingest to Processing -->
            <line x1="30%" y1="30%" x2="40%" y2="50%" stroke="#64748b" stroke-width="4" marker-end="url(#arrowhead)" />
            <line x1="30%" y1="70%" x2="40%" y2="50%" stroke="#64748b" stroke-width="4" marker-end="url(#arrowhead)" />
            <!-- Processing to Outputs -->
            <line x1="60%" y1="50%" x2="70%" y2="25%" stroke="#64748b" stroke-width="4" marker-end="url(#arrowhead)" />
            <line x1="60%" y1="50%" x2="70%" y2="50%" stroke="#64748b" stroke-width="4" marker-end="url(#arrowhead)" />
            <line x1="60%" y1="50%" x2="70%" y2="75%" stroke="#64748b" stroke-width="4" marker-end="url(#arrowhead)" />
        </svg>

        <div class="flow-container">
            <!-- Left Column -->
            <div class="flow-col" style="align-items: flex-end;">
                <div class="box box-red">Baltic Index &<br>Live AIS Stream</div>
                <div class="box box-blue">Port Trust<br>Tidal Circulars</div>
            </div>
            
            <!-- Center Column -->
            <div class="large-box">
                <div class="lb-title">Adaptive Signal Processing</div>
                <div class="lb-item">Data Harmonization & Validation</div>
                <div class="lb-item">Holt-Winters Core (Decomposition)</div>
                <div class="lb-item">SciPy UKC Solver (Tidal Berth Intake)</div>
                <div class="lb-item" style="margin-bottom:0;">Continuous Market Tracking</div>
            </div>
            
            <!-- Right Column -->
            <div class="flow-col" style="align-items: flex-start;">
                <div class="box box-purple">10k Monte Carlo<br>Volatility Bounds</div>
                <div class="box box-green">Market Entry Score<br>& Demurrage Shield</div>
                <div class="box box-red">Decision Output:<br>Spot vs COA Hedge</div>
            </div>
        </div>
    </div>
    
    <div class="bottom-section">
        <div class="bottom-left">
            <div class="section-title" style="margin-bottom: 10px;">3 LAYER APPROACH</div>
            <div style="position: relative; width: 100%; height: 100%;">
                <div class="layer layer-3">Layer 3: Decision Shield</div>
                <div class="layer layer-2">Layer 2: AI Forecasting</div>
                <div class="layer layer-1">Layer 1: Data Ingestion</div>
                
                <!-- Connector lines & labels -->
                <svg style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:0;" xmlns="http://www.w3.org/2000/svg">
                    <!-- Lines connecting layers to labels -->
                    <path d="M 330 130 L 360 130" stroke="#475569" stroke-width="3" fill="none"/>
                    <path d="M 370 90 L 400 90" stroke="#475569" stroke-width="3" fill="none"/>
                    <path d="M 410 50 L 440 50" stroke="#475569" stroke-width="3" fill="none"/>
                </svg>
                
                <div class="layer-label ll-1">GNSS / API</div>
                <div class="layer-label ll-2">LEO-PNT / AI</div>
                <div class="layer-label ll-3">INS / DECISION</div>
            </div>
        </div>
        
        <div class="bottom-right">
            <div class="link-row">GitHub link: <br><span class="link-url">https://github.com/futuristics/FreightForecast.git</span></div>
            <div class="link-row">YouTube video: <span class="link-url-yt">Link</span></div>
            <div class="status-row">Above 80% of the prototype is completed</div>
        </div>
    </div>
    
</div>
</body>
</html>
"""

async def generate_image():
    out_file = "sih_slide3_body.png"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        temp_file = "temp_sih_3_custom.html"
        
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(HTML_SLIDE_3_CUSTOM)
            
        page = await browser.new_page(
            viewport={"width": 1420, "height": 670},
            device_scale_factor=2.5
        )
        
        file_url = f"file:///{os.path.abspath(temp_file).replace(chr(92), '/')}"
        await page.goto(file_url, wait_until="networkidle")
        await asyncio.sleep(0.5)
        
        container = page.locator(".wrapper")
        await container.screenshot(path=os.path.join(r"c:\\vs studio\\freight-forecast", out_file), type="png", omit_background=True)
        print(f"Rendered custom {out_file}")
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_image())
