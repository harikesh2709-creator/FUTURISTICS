import os
from playwright.sync_api import sync_playwright

PROBLEM_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0; padding: 0; background: transparent;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    width: 600px; height: 850px;
    display: flex; justify-content: center; align-items: center;
  }
  .container {
    display: flex; flex-direction: column; width: 100%; height: 100%; align-items: center; justify-content: space-between;
    padding: 10px; box-sizing: border-box;
  }
  .card {
    width: 100%; height: 350px; border-radius: 16px;
    display: flex; flex-direction: column;
    box-shadow: 0 12px 24px rgba(0,0,0,0.12);
    overflow: hidden;
  }
  .card-header {
    height: 70px; display: flex; align-items: center; justify-content: center;
    font-size: 26px; font-weight: 800; color: white; letter-spacing: 1px;
    text-transform: uppercase;
  }
  .card-body {
    flex: 1; padding: 20px 30px; display: flex; flex-direction: column; justify-content: space-around;
  }
  .item {
    display: flex; align-items: center; font-size: 23px; font-weight: 700;
  }
  .icon {
    width: 36px; height: 36px; border-radius: 50%; display: flex; justify-content: center; align-items: center;
    margin-right: 18px; color: white; font-weight: bold; font-size: 22px;
    flex-shrink: 0;
  }

  /* Current State (Red/Gray) */
  .c-current { background: #FFFFFF; border: 3px solid #E2E8F0; }
  .c-current .card-header { background: linear-gradient(135deg, #EF4444, #991B1B); }
  .c-current .icon { background: #EF4444; }
  .c-current .text { color: #334155; }

  /* Spectra State (Green/Blue) */
  .c-spectra { background: #F0FDF4; border: 3px solid #86EFAC; }
  .c-spectra .card-header { background: linear-gradient(135deg, #10B981, #047857); }
  .c-spectra .icon { background: #10B981; }
  .c-spectra .text { color: #064E3B; }

  /* Arrow Down */
  .transition {
    width: 100%; height: 110px; display: flex; align-items: center; justify-content: center; position: relative;
  }
  .arrow-body {
    width: 36px; height: 60px; background: #94A3B8; position: relative; border-radius: 6px 6px 0 0;
    display: flex; justify-content: center; align-items: center;
  }
  .arrow-body::after {
    content: ''; position: absolute; bottom: -38px; left: -17px;
    border-left: 35px solid transparent; border-right: 35px solid transparent; 
    border-top: 40px solid #94A3B8;
  }
  .trans-text {
    position: absolute; left: 340px; font-size: 22px; font-weight: 800; color: #475569; text-align: left;
    text-transform: uppercase; letter-spacing: 1px;
  }
</style>
</head>
<body>
  <div class="container">
    <!-- Current -->
    <div class="card c-current">
      <div class="card-header">Current Scenario</div>
      <div class="card-body">
        <div class="item"><div class="icon">✕</div><div class="text">Manual Signal Triage</div></div>
        <div class="item"><div class="icon">✕</div><div class="text">High Latency Analysis</div></div>
        <div class="item"><div class="icon">✕</div><div class="text">Human Error Vulnerability</div></div>
        <div class="item"><div class="icon">✕</div><div class="text">No Blind AMC / FEC Solvers</div></div>
      </div>
    </div>

    <!-- Arrow -->
    <div class="transition">
      <div class="arrow-body"></div>
      <div class="trans-text">SPECTRA<br>PARADIGM</div>
    </div>

    <!-- Spectra -->
    <div class="card c-spectra">
      <div class="card-header">SPECTRA Architecture</div>
      <div class="card-body">
        <div class="item"><div class="icon">✓</div><div class="text">100% Autonomous Pipeline</div></div>
        <div class="item"><div class="icon">✓</div><div class="text">Sub-Second Classification</div></div>
        <div class="item"><div class="icon">✓</div><div class="text">AI-Driven Extraction</div></div>
        <div class="item"><div class="icon">✓</div><div class="text">Galois Field Blind Solving</div></div>
      </div>
    </div>
  </div>
</body>
</html>
"""

def generate():
    assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
    os.makedirs(assets_dir, exist_ok=True)
    out = os.path.join(assets_dir, 'problem_statement_graphic.png')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using 2x scale factor for crisp text (already large natively)
        page = browser.new_page(viewport={"width": 600, "height": 850}, device_scale_factor=2)
        page.set_content(PROBLEM_HTML)
        page.wait_for_timeout(300)
        page.screenshot(path=out, omit_background=True)
        browser.close()
        print(f"Generated: {out}")

if __name__ == "__main__":
    generate()
