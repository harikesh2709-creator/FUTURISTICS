import os
from playwright.sync_api import sync_playwright

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 800px;
    height: 800px;
  }
  .container {
    width: 100%;
    height: 100%;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle, #ffffff 0%, #f8fafc 100%);
  }
  
  .tier {
    width: 100%;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    overflow: hidden;
    position: relative;
  }
  
  .t1 { background: #F0F7FF; border: 2px solid #93C5FD; height: 28%; }
  .t2 { background: #F0FDF4; border: 2px solid #86EFAC; height: 35%; }
  .t3 { background: #FAF5FF; border: 2px solid #D8B4FE; height: 28%; }

  .tier-title {
    padding: 10px;
    text-align: center;
    font-weight: 800;
    font-size: 16px;
    letter-spacing: 1px;
    color: #FFFFFF;
    text-transform: uppercase;
  }
  .t1 .tier-title { background: #1E40AF; }
  .t2 .tier-title { background: #0F766E; }
  .t3 .tier-title { background: #7C3AED; }

  .content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    padding: 15px;
    height: 100%;
  }
  
  .card {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .t1 .card { border: 1.5px solid #BFDBFE; }
  .t2 .card { border: 1.5px solid #A7F3D0; }
  .t3 .card { border: 1.5px solid #E9D5FF; }

  .card-title {
    font-size: 15px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card-desc {
    font-size: 13px;
    color: #475569;
    line-height: 1.4;
  }
  
  .badge {
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 800;
  }
  .b-blue { background: #DBEAFE; color: #1E40AF; }
  .b-teal { background: #CCFBF1; color: #0F766E; }
  .b-purple { background: #EDE9FE; color: #6D28D9; }

  .connector-arrow {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 40px;
  }
</style>
</head>
<body>

<div class="container">
  
  <!-- TIER 1 -->
  <div class="tier t1">
    <div class="tier-title">TIER 1: DATA INGESTION</div>
    <div class="content-grid">
      <div class="card">
        <div class="card-title"><span class="badge b-blue">API</span> Baltic Exchange</div>
        <div class="card-desc">BDI, Capesize, Panamax Indices</div>
      </div>
      <div class="card">
        <div class="card-title"><span class="badge b-blue">AIS</span> Fleet Telemetry</div>
        <div class="card-desc">Live Spire AIS: SOG, Heading, Draft</div>
      </div>
    </div>
  </div>

  <div class="connector-arrow">
    <svg width="40" height="40" viewBox="0 0 40 40">
      <defs>
        <marker id="arr1" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
          <polygon points="0 0, 6 3, 0 6" fill="#64748B" />
        </marker>
      </defs>
      <line x1="20" y1="0" x2="20" y2="35" stroke="#64748B" stroke-width="4" stroke-dasharray="6,4" marker-end="url(#arr1)" />
    </svg>
  </div>

  <!-- TIER 2 -->
  <div class="tier t2">
    <div class="tier-title">TIER 2: AI CORE ENGINES</div>
    <div class="content-grid">
      <div class="card">
        <div class="card-title"><span class="badge b-teal">ML</span> Holt-Winters Engine</div>
        <div class="card-desc">90D Forward Forecast (1.7% MAPE)</div>
      </div>
      <div class="card">
        <div class="card-title"><span class="badge b-teal">MATH</span> Monte Carlo Sim</div>
        <div class="card-desc">10k Runs for Confidence Bounds</div>
      </div>
      <div class="card">
        <div class="card-title"><span class="badge b-teal">SOLVE</span> Dynamic UKC</div>
        <div class="card-desc">Tidal Clearance Optimization</div>
      </div>
      <div class="card">
        <div class="card-title"><span class="badge b-teal">DB</span> Spatial Redis Cache</div>
        <div class="card-desc">Sub-35ms Analytics Processing</div>
      </div>
    </div>
  </div>

  <div class="connector-arrow">
    <svg width="40" height="40" viewBox="0 0 40 40">
      <defs>
        <marker id="arr2" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
          <polygon points="0 0, 6 3, 0 6" fill="#64748B" />
        </marker>
      </defs>
      <line x1="20" y1="0" x2="20" y2="35" stroke="#64748B" stroke-width="4" stroke-dasharray="6,4" marker-end="url(#arr2)" />
    </svg>
  </div>

  <!-- TIER 3 -->
  <div class="tier t3">
    <div class="tier-title">TIER 3: REACT DASHBOARD</div>
    <div class="content-grid">
      <div class="card">
        <div class="card-title"><span class="badge b-purple">CHART</span> Predictive Curves</div>
        <div class="card-desc">Interactive Forecast Trajectories</div>
      </div>
      <div class="card">
        <div class="card-title"><span class="badge b-purple">MAP</span> Live AIS GIS</div>
        <div class="card-desc">Vessel Port Queue Tracking</div>
      </div>
    </div>
  </div>

</div>

</body>
</html>
"""

def render_diagram():
    out_png = r"c:\vs studio\freight-forecast\slide2_center_architecture.png"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 800, "height": 800}, device_scale_factor=2)
        page.set_content(HTML_CONTENT)
        page.wait_for_timeout(300)
        page.screenshot(path=out_png)
        browser.close()
    print(f"Generated center architecture diagram to: {out_png}")

if __name__ == "__main__":
    render_diagram()
