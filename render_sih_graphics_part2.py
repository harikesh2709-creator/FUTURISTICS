import asyncio
from playwright.async_api import async_playwright
import os

HTML_SLIDE_3 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; width: 1400px; height: 650px; overflow: hidden; }
        .wrapper { display: flex; flex-direction: column; gap: 20px; padding: 10px; width: 100%; height: 100%; box-sizing: border-box; }
        
        .row-top { display: flex; flex-direction: column; gap: 10px; }
        .row-bottom { display: flex; gap: 20px; flex: 1; }
        
        .arch-title { background: #1e3a8a; color: white; padding: 12px; text-align: center; font-weight: 800; font-size: 16px; border-radius: 8px; letter-spacing: 0.5px; }
        .zones { display: flex; gap: 15px; }
        .zone-box { flex: 1; border: 2px solid #cbd5e1; border-radius: 10px; background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05); overflow: hidden; }
        .z-head { padding: 10px; text-align: center; font-weight: 800; font-size: 14px; color: white; }
        .z-body { padding: 15px; text-align: center; font-size: 14px; color: #1e293b; font-weight: 500; line-height: 1.4; display: flex; align-items: center; justify-content: center; height: 70px; }
        
        .z1 { background: #1d4ed8; }
        .z2 { background: #3b82f6; }
        .z3 { background: #059669; }
        .z4 { background: #15803d; }
        
        .col-left { flex: 0.45; display: flex; flex-direction: column; gap: 10px; }
        .col-right { flex: 0.55; display: flex; flex-direction: column; gap: 10px; }
        
        .sec-title { background: #1e3a8a; color: white; padding: 12px; text-align: center; font-weight: 800; font-size: 16px; border-radius: 8px; letter-spacing: 0.5px; }
        .sec-title.green { background: #15803d; }
        
        .stage-box { border: 2px solid #e2e8f0; border-radius: 8px; padding: 12px 15px; background: white; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
        .s-title { font-size: 15px; font-weight: 800; color: #0f172a; margin-bottom: 5px; }
        .s-hl { color: #2563eb; }
        .s-hl2 { color: #059669; }
        .s-hl3 { color: #dc2626; }
        .s-hl4 { color: #d97706; }
        .s-desc { font-size: 13.5px; color: #475569; font-weight: 500; line-height: 1.4; }
        
        .math-box { border: 2px solid #bfdbfe; border-radius: 8px; padding: 15px; background: white; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.03); display: flex; justify-content: center; align-items: center; }
        .math-txt { font-family: 'Consolas', monospace; font-size: 16px; font-weight: 800; color: #1e3a8a; }
        .math-sep { margin: 0 15px; color: #94a3b8; }
        
        .proto-placeholder { flex: 1; border: 2px dashed #94a3b8; border-radius: 8px; background: #f8fafc; display: flex; justify-content: space-around; align-items: center; font-weight: 700; color: #15803d; }
    </style>
</head>
<body>
<div class="wrapper">
    
    <div class="row-top">
        <div class="arch-title">4-ZONE ENTERPRISE MARITIME ARCHITECTURE (END-TO-END FLOW)</div>
        <div class="zones">
            <div class="zone-box">
                <div class="z-head z1">ZONE 1: Telemetry & Ingestion</div>
                <div class="z-body">Baltic Exchange BDI/BCI/BPI/BSI feeds, Satellite AIS vessel tracking, Major Port circulars.</div>
            </div>
            <div class="zone-box">
                <div class="z-head z2">ZONE 2: Presentation Layer</div>
                <div class="z-body">React 19 / Next.js SPA, Chart.js multi-horizon curves, Leaflet.js interactive GIS map.</div>
            </div>
            <div class="zone-box">
                <div class="z-head z3">ZONE 3: High-Speed Core API</div>
                <div class="z-body">Python FastAPI asynchronous framework, Uvicorn ASGI, Redis In-Memory sub-35ms Cache.</div>
            </div>
            <div class="zone-box">
                <div class="z-head z4">ZONE 4: AI & Math Engine</div>
                <div class="z-body">Statsmodels Holt-Winters, 10,000 Monte Carlo runs, Landed $/MT solver, UKC tidal check.</div>
            </div>
        </div>
    </div>
    
    <div class="row-bottom">
        <div class="col-left">
            <div class="sec-title">IMPLEMENTATION PROCESS & PIPELINE STAGES</div>
            
            <div class="stage-box">
                <div class="s-title"><span class="s-hl">[STAGE 1]</span> Data Harmonization & ETL</div>
                <div class="s-desc">Aggregates 1,825 daily Baltic records with live Port Trust draft circulars into schema-validated PostgreSQL tables.</div>
            </div>
            <div class="stage-box">
                <div class="s-title"><span class="s-hl2">[STAGE 2]</span> Triple Seasonal Decomposition</div>
                <div class="s-desc">Holt-Winters isolates monsoon & commodity cycles: Level ℓ(t), Trend b(t), Seasonal s(t) with MAPE 1.7%.</div>
            </div>
            <div class="stage-box">
                <div class="s-title"><span class="s-hl3">[STAGE 3]</span> Physical Berth Draught Safety</div>
                <div class="s-desc">Validates dynamic Under-Keel Clearance: UKC = (Charted Depth + Astronomical Tide) - Arrival Draft &ge; 1.5m.</div>
            </div>
            <div class="stage-box">
                <div class="s-title"><span class="s-hl4">[STAGE 4]</span> Decision Advisory & Contract Hedging</div>
                <div class="s-desc">Mixed Integer Solver ranks $/MT landed cost across corridors; recommends optimal Spot vs COA forward fixtures.</div>
            </div>
        </div>
        
        <div class="col-right">
            <div class="sec-title green">MATHEMATICAL FORMULATION & LIVE PROTOTYPE ENGINE</div>
            <div class="math-box">
                <div class="math-txt">Holt-Winters: Y(t+h) = [ℓ(t) + h&middot;b(t)] &times; s(t+h-m) <span class="math-sep">|</span> Min $/MT = [(Hire&times;Days)+Fuel+Dues] &divide; Cargo MT</div>
            </div>
            
            <div class="proto-placeholder">
                <div>Live Multi-Route Draught Matrix</div>
                <div>Suez vs Cape Canal Optimizer</div>
            </div>
        </div>
    </div>

</div>
</body>
</html>
"""

HTML_SLIDE_7 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; width: 1400px; height: 650px; overflow: hidden; }
        .wrapper { display: flex; flex-direction: column; gap: 20px; padding: 10px; width: 100%; height: 100%; box-sizing: border-box; }
        
        .row-top { display: flex; gap: 20px; flex: 1; }
        .mod-col { flex: 1; display: flex; flex-direction: column; gap: 10px; border: 2px solid #1e3a8a; border-radius: 15px; padding: 2px; overflow: hidden; background: white; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
        .mod-col.green { border-color: #15803d; }
        
        .mod-title { background: #1e3a8a; color: white; font-weight: 800; font-size: 15px; padding: 15px; text-align: center; letter-spacing: 0.5px; border-radius: 12px 12px 0 0; text-transform: uppercase; }
        .mod-col.green .mod-title { background: #15803d; }
        
        .mod-content { flex: 1; background: #0f172a; margin: 0 2px; border-radius: 4px; display: flex; align-items: center; justify-content: center; }
        .mod-desc { padding: 12px; font-style: italic; font-size: 14px; text-align: center; color: #475569; font-weight: 500; }
        
        .row-bottom { display: flex; flex-direction: column; gap: 10px; }
        .stack-title { background: #0f172a; color: white; font-weight: 800; font-size: 16px; padding: 14px; text-align: center; letter-spacing: 1px; border-radius: 8px; text-transform: uppercase; }
        
        .stack-boxes { display: flex; gap: 20px; padding: 15px 25px; background: white; border-radius: 12px; border: 2px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .stack-col { flex: 1; }
        .s-head { font-weight: 800; font-size: 16px; color: #2563eb; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }
        .s-item { font-size: 14.5px; font-weight: 600; color: #1e293b; margin-bottom: 10px; display: flex; align-items: center; }
        .s-check { color: #15803d; font-weight: 900; margin-right: 8px; font-size: 16px; }
        
        .footer { background: #1e3a8a; color: white; text-align: center; padding: 12px; font-weight: 700; font-size: 15px; border-radius: 8px; margin-top: 5px; }
    </style>
</head>
<body>
<div class="wrapper">
    
    <div class="row-top">
        <div class="mod-col">
            <div class="mod-title">MODULE 1: AI RATE FORECASTING & 90-DAY VOLATILITY CURVES</div>
            <div class="mod-content" style="background: url('media_1788176868086.png') no-repeat center center; background-size: cover;">
                <!-- Embedded dark screenshot from prototype -->
            </div>
            <div class="mod-desc">Interactive 90-day Holt-Winters predictive curves across Capesize, Panamax & Supramax vessels.</div>
        </div>
        
        <div class="mod-col green">
            <div class="mod-title">MODULE 2: LIVE AIS FLEET TELEMATICS & PORT CONGESTION</div>
            <div class="mod-content" style="background: url('media_1788176955634.png') no-repeat center center; background-size: cover;">
                 <!-- Embedded dark screenshot from prototype map -->
            </div>
            <div class="mod-desc">Live AIS vessel position tracking, real-time berth draught verification & congestion monitor.</div>
        </div>
    </div>
    
    <div class="row-bottom">
        <div class="stack-title">PRODUCTION-GRADE TECHNOLOGY STACK & ARCHITECTURAL PILLARS</div>
        <div class="stack-boxes">
            <div class="stack-col">
                <div class="s-head">Frontend / GIS</div>
                <div class="s-item"><span class="s-check">&#10004;</span> React 19 / Next.js</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Tailwind CSS Design System</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Chart.js Predictive Curves</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Leaflet.js Dynamic GIS Map</div>
            </div>
            <div class="stack-col">
                <div class="s-head" style="color: #059669;">Backend / API</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Python FastAPI Async</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Uvicorn ASGI Server</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Redis Sub-35ms Cache</div>
                <div class="s-item"><span class="s-check">&#10004;</span> PostgreSQL / PostGIS Engine</div>
            </div>
            <div class="stack-col">
                <div class="s-head" style="color: #ea580c;">AI / Math Engine</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Holt-Winters Seasonal Model</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Monte Carlo 10K Simulation</div>
                <div class="s-item"><span class="s-check">&#10004;</span> UKC Astronomical Tidal Solver</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Landed $/MT Linear Program</div>
            </div>
            <div class="stack-col">
                <div class="s-head" style="color: #7c3aed;">Cloud / DevOps</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Docker Containerization</div>
                <div class="s-item"><span class="s-check">&#10004;</span> AWS EC2 / GCP Cloud Run</div>
                <div class="s-item"><span class="s-check">&#10004;</span> Automated GitHub Actions CI</div>
                <div class="s-item"><span class="s-check">&#10004;</span> 99.9% Uptime Production SLA</div>
            </div>
        </div>
        
        <div class="footer">
            TEAM FUTURISTICS | End-to-End Functional Prototype Tested & Validated Across 6 Global Dry Bulk Corridors | SIH 2026 Final Round
        </div>
    </div>

</div>
</body>
</html>
"""

async def generate_images():
    html_files = {
        "sih_slide3_body.png": HTML_SLIDE_3,
        "sih_slide7_body.png": HTML_SLIDE_7
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for out_file, html_content in html_files.items():
            temp_file = "temp_sih_2.html"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            page = await browser.new_page(
                viewport={"width": 1420, "height": 670},
                device_scale_factor=2.5
            )
            
            file_url = f"file:///{os.path.abspath(temp_file).replace(chr(92), '/')}"
            await page.goto(file_url, wait_until="networkidle")
            
            await asyncio.sleep(0.5)
            
            container = page.locator(".wrapper")
            await container.screenshot(path=os.path.join(r"c:\vs studio\freight-forecast", out_file), type="png", omit_background=True)
            print(f"Rendered {out_file}")
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_images())
