import os
from playwright.sync_api import sync_playwright

FLOWCHART_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    width: 1000px;
    height: 450px;
    position: relative;
  }
  
  /* Text defaults */
  .text {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-size: 15px;
  }
  
  .small-text {
    position: absolute;
    font-size: 13px;
    color: #1E293B;
    font-weight: 700;
    background: #FFFFFF;
    padding: 3px 6px;
    border-radius: 4px;
    border: 1px solid #CBD5E1;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    line-height: 1.1;
  }

  /* Boxes */
  .box {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 6px;
    line-height: 1.25;
    letter-spacing: 0.2px;
  }
  
  .solid-box {
    color: #FFFFFF;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    font-weight: 700;
  }

  /* Modern SIGINT Palette */
  .bg-primary { background: linear-gradient(135deg, #1E40AF, #1E3A8A); border: 2px solid #172554; } 
  .bg-secondary { background: linear-gradient(135deg, #475569, #334155); border: 2px solid #1E293B; } 
  .bg-accent { background: linear-gradient(135deg, #059669, #047857); border: 2px solid #064E3B; }
  .bg-highlight { background: linear-gradient(135deg, #7C3AED, #6D28D9); border: 2px solid #4C1D95; }
  
  .bg-container-1 { 
    background: #F0F9FF; 
    border: 2px dashed #7DD3FC; 
    border-radius: 12px; 
    color: #0369A1; 
    font-weight: 800; 
  }
  .bg-container-2 { 
    background: #F8FAFC; 
    border: 2px dashed #94A3B8; 
    border-radius: 12px; 
    color: #475569; 
    font-weight: 800; 
  }
  
  .inner-box {
    background: #FFFFFF;
    color: #0F172A;
    border: 1.5px solid #94A3B8;
    border-radius: 6px;
    font-weight: 600;
    box-shadow: 0 2px 5px rgba(0,0,0,0.08);
  }

  /* Specific Box Placements - Expanded sizes for better clarity */
  #box-left-white { left: 20px; top: 180px; width: 90px; height: 65px; font-size: 16px; }
  #box-gnss { left: 150px; top: 50px; width: 140px; height: 80px; font-size: 24px; }
  #box-pnt-teal { left: 300px; top: 25px; width: 90px; height: 50px; font-size: 15px; }
  #box-leosoo { left: 175px; top: 175px; width: 100px; height: 55px; font-size: 15px; }
  
  /* Blue Container */
  #container-blue { left: 520px; top: 25px; width: 450px; height: 185px; align-items: flex-start; justify-content: center; padding-top: 10px; font-size: 16px; text-transform: uppercase; letter-spacing: 0.5px; }
  
  /* Inner Teal Boxes (Blue container) - Bigger Text */
  .inner-teal { width: 110px; height: 45px; font-size: 14px; }
  #b-orbit { left: 535px; top: 75px; }
  #b-motion { left: 675px; top: 65px; width: 90px; height: 55px; }
  #b-rf { left: 795px; top: 75px; width: 105px; height: 45px; }
  #b-noise { left: 685px; top: 145px; width: 150px; height: 45px; }
  #b-compare { left: 530px; top: 145px; width: 130px; height: 45px; }

  /* Purple Container */
  #container-purple { left: 330px; top: 145px; width: 175px; height: 275px; align-items: flex-start; justify-content: center; padding-top: 10px; font-size: 15px; text-transform: uppercase; letter-spacing: 0.5px; }
  
  /* Inner Pink Boxes (Purple container) - Bigger Text */
  .inner-pink { left: 345px; width: 145px; height: 40px; font-size: 14px; }
  #p1 { top: 180px; }
  #p2 { top: 225px; }
  #p3 { top: 270px; }
  #p4 { top: 315px; }
  #p5 { top: 360px; }

  /* Standalone Pink */
  #box-standalone-pink { left: 530px; top: 255px; width: 150px; height: 50px; font-size: 14px; }
  
  /* SVG for arrows */
  svg {
    position: absolute;
    top: 0; left: 0; width: 1000px; height: 450px; pointer-events: none;
  }
  path, line {
    fill: none;
    stroke: #64748B;
    stroke-width: 3px; /* Thicker arrows */
    stroke-linejoin: round;
  }
  .arr-green { stroke: #0284C7; } /* using blue instead of green for modern look */

  /* Arrowheads */
  .arrow-head { fill: #64748B; stroke: none; }
  .arrow-head-green { fill: #0284C7; stroke: none; }

</style>
</head>
<body>

<!-- Arrows Layer -->
<svg>
  <defs>
    <marker id="arrow" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto-start-reverse">
      <polygon points="0 0, 5 2.5, 0 5" class="arrow-head" />
    </marker>
    <marker id="arrow-green" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto-start-reverse">
      <polygon points="0 0, 5 2.5, 0 5" class="arrow-head-green" />
    </marker>
  </defs>

  <!-- Green arrows to left white box -->
  <line x1="175" y1="200" x2="110" y2="200" class="arr-green" marker-end="url(#arrow-green)" />
  <path d="M 150 90 L 130 90 L 130 200" class="arr-green" />

  <!-- GNSS to PNT Teal (up right) -->
  <path d="M 290 90 L 345 90 L 345 75" marker-end="url(#arrow)" />
  
  <!-- GNSS to LEO SoO (down) -->
  <line x1="220" y1="130" x2="220" y2="175" marker-end="url(#arrow)" />
  <!-- PNT Teal to Orbit Modeling (horizontal) -->
  <line x1="390" y1="50" x2="590" y2="50" />
  <line x1="590" y1="50" x2="590" y2="75" marker-end="url(#arrow)" />

  <!-- Inside Blue Box -->
  <line x1="645" y1="95" x2="675" y2="95" marker-end="url(#arrow)" />
  <line x1="765" y1="95" x2="795" y2="95" marker-end="url(#arrow)" />
  <path d="M 900 95 L 930 95 L 930 165 L 835 165" marker-end="url(#arrow)" />
  <line x1="685" y1="165" x2="660" y2="165" marker-end="url(#arrow)" />
  
  <!-- Compare to Orbit (Up) -->
  <line x1="590" y1="145" x2="590" y2="120" marker-end="url(#arrow)" />

  <!-- Compare to Signal Processing (Left) -->
  <path d="M 530 165 L 515 165 L 515 197 L 490 197" marker-end="url(#arrow)" />

  <!-- Inside Purple Box (Down arrows) -->
  <line x1="415" y1="220" x2="415" y2="225" marker-end="url(#arrow)" />
  <line x1="415" y1="265" x2="415" y2="270" marker-end="url(#arrow)" />
  <line x1="415" y1="310" x2="415" y2="315" marker-end="url(#arrow)" />
  <line x1="415" y1="355" x2="415" y2="360" marker-end="url(#arrow)" />

  <!-- Standalone Pink to Pseudorange -->
  <line x1="530" y1="280" x2="490" y2="280" marker-end="url(#arrow)" />

  <!-- Tracking to LEO SoO -->
  <path d="M 345 380 L 315 380 L 315 200 L 275 200" marker-end="url(#arrow)" />

</svg>

<!-- Boxes -->
<div class="box solid-box bg-accent" id="box-left-white">Decoded<br>Bits</div>
<div class="box solid-box bg-primary" id="box-gnss">Raw .IQ<br>.wav</div>
<div class="box solid-box bg-secondary" id="box-pnt-teal">Pre-<br>Process</div>
<div class="box solid-box bg-secondary" id="box-leosoo">Demod<br>Core</div>

<div class="box bg-blue-container" id="container-blue">Autonomous Parameter Extraction & AMC</div>
<div class="box inner-box inner-teal" id="b-orbit">Welch PSD &<br>FFT</div>
<div class="box inner-box inner-teal" id="b-motion">Cyclo CAF</div>
<div class="box inner-box inner-teal" id="b-rf">Cumulants</div>
<div class="box inner-box inner-teal" id="b-noise">1D-CNN + Bi-LSTM<br>Model</div>
<div class="box inner-box inner-teal" id="b-compare">Class Confidence</div>

<div class="box bg-purple-container" id="container-purple">Blind Sync & FEC Decoding</div>
<div class="box inner-box inner-pink" id="p1">Gardner Timing TED</div>
<div class="box inner-box inner-pink" id="p2">Costas Loop Sync</div>
<div class="box inner-box inner-pink" id="p3">Galois Field Solver</div>
<div class="box inner-box inner-pink" id="p4">Viterbi Trellis Decode</div>
<div class="box inner-box inner-pink" id="p5">Reed-Solomon Decode</div>

<div class="box solid-box bg-highlight" id="box-standalone-pink">Cryptographic<br>SHA-256 Audit</div>

<!-- Text Labels -->
<div class="small-text" style="left:230px; top:145px;">No signal</div>
<div class="small-text" style="left:110px; top:178px; color:#0284C7;">Signal Data</div>
<div class="small-text" style="left:305px; top:75px;">For extraction</div>
<div class="small-text" style="left:415px; top:15px; width: 120px; text-align:center;">Avoiding manual<br>triage bottlenecks</div>
<div class="small-text" style="left:600px; top:130px;">&lt; 95% matches</div>
<div class="small-text" style="left:535px; top:200px;">&gt; 95% matches</div>

</body>
</html>
"""

LAYER_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0; padding: 0; background: transparent;
    font-family: system-ui, -apple-system, sans-serif;
    width: 400px; height: 185px;
    position: relative;
  }
  .title {
    font-size: 16px; font-weight: 800; color: #1E3A8A;
    text-transform: uppercase; margin-bottom: 20px;
    letter-spacing: 0.5px;
  }
  /* The 3 rectangles */
  .rect {
    position: absolute; width: 180px; height: 90px;
    box-shadow: 2px 4px 8px rgba(0,0,0,0.2);
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.2);
  }
  .r1 { left: 20px; top: 40px; background: linear-gradient(135deg, #047857, #064E3B); } /* green */
  .r2 { left: 35px; top: 60px; background: linear-gradient(135deg, #BE123C, #881337); } /* red */
  .r3 { left: 50px; top: 80px; background: linear-gradient(135deg, #1D4ED8, #1E3A8A); } /* blue */

  /* Labels */
  .lbl {
    position: absolute;
    background: #FFFFFF; border: 1.5px solid #CBD5E1;
    padding: 4px 8px; font-size: 14px; color: #0F172A;
    border-radius: 4px; font-weight: 700;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }
  #l1 { left: 230px; top: 30px; }
  #l2 { left: 260px; top: 90px; }
  #l3 { left: 230px; top: 140px; }

  /* Arrows */
  svg {
    position: absolute; top:0; left:0; width: 400px; height: 185px; pointer-events: none;
    z-index: 10;
  }
  path, line { fill: none; stroke: #64748B; stroke-width: 3px; }
  .arrow-head { fill: #64748B; stroke: none; }
</style>
</head>
<body>
  <div class="title" style="margin-left: 20px; margin-top: 10px;">3 LAYER ARCHITECTURE</div>

  <div class="rect r1"></div>
  <div class="rect r2"></div>
  <div class="rect r3"></div>

  <svg>
    <defs>
      <marker id="arrow" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto-start-reverse">
        <polygon points="0 0, 5 2.5, 0 5" class="arrow-head" />
      </marker>
    </defs>
    <!-- From green (back) to l1 -->
    <path d="M 120 40 L 120 35 L 225 35" marker-end="url(#arrow)" />
    <!-- From red (middle) to l2 -->
    <path d="M 215 75 L 230 75 L 230 100 L 255 100" marker-end="url(#arrow)" />
    <!-- From blue (front) to l3 -->
    <path d="M 230 120 L 245 120 L 245 150 L 225 150" marker-end="url(#arrow)" />
  </svg>

  <div class="lbl" id="l1">Physical & MAC</div>
  <div class="lbl" id="l2">Feature AMC</div>
  <div class="lbl" id="l3">GF(2) Decoders</div>
</body>
</html>
"""

def generate():
    assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
    os.makedirs(assets_dir, exist_ok=True)
    out_flow = os.path.join(assets_dir, 'system_architecture_drawio.png')
    out_3layer = os.path.join(assets_dir, 'spectra_3layer_approach.png')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Flowchart
        page1 = browser.new_page(viewport={"width": 1000, "height": 450}, device_scale_factor=2)
        page1.set_content(FLOWCHART_HTML)
        page1.wait_for_timeout(300)
        page1.screenshot(path=out_flow, omit_background=True)
        print(f"Exported exact reference style flowchart: {out_flow}")
        
        # 3 Layer
        page2 = browser.new_page(viewport={"width": 400, "height": 185}, device_scale_factor=2)
        page2.set_content(LAYER_HTML)
        page2.wait_for_timeout(300)
        page2.screenshot(path=out_3layer, omit_background=True)
        print(f"Exported exact reference style 3-layer approach: {out_3layer}")
        
        browser.close()

if __name__ == "__main__":
    generate()
