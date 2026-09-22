"""
Render Official UN SDG Goals Central Badge for SIH 2026 Presentation
Features:
- Official UN SDG 17-Color Ring Wheel
- Official UN SDG 9 (Industry, Innovation & Infrastructure - #F36D25)
- Official UN SDG 12 (Responsible Consumption & Production - #CF8D2A)
- Official UN SDG 13 (Climate Action - #48773E)
- Bold Typography & High-Contrast Metrics
"""

import math
from playwright.sync_api import sync_playwright

SDG_COLORS = [
    "#E5243B", "#DDA63A", "#4C9F38", "#C5192D", "#FF3A21",
    "#26BDE2", "#FCC30B", "#A21942", "#FD6925", "#DD1367",
    "#FD9D24", "#BF8B2E", "#3F7E44", "#0A97D9", "#56C02B",
    "#00689D", "#19486A"
]

def generate_sdg_wheel_svg(cx=60, cy=60, r_in=30, r_out=54):
    n = 17
    paths = []
    angle_step = 360.0 / n
    for i in range(n):
        a1 = math.radians(i * angle_step - 90)
        a2 = math.radians((i + 1) * angle_step - 90)
        
        x1_out = cx + r_out * math.cos(a1)
        y1_out = cy + r_out * math.sin(a1)
        x2_out = cx + r_out * math.cos(a2)
        y2_out = cy + r_out * math.sin(a2)
        
        x1_in = cx + r_in * math.cos(a1)
        y1_in = cy + r_in * math.sin(a1)
        x2_in = cx + r_in * math.cos(a2)
        y2_in = cy + r_in * math.sin(a2)
        
        d = (
            f"M {x1_out:.2f} {y1_out:.2f} "
            f"A {r_out} {r_out} 0 0 1 {x2_out:.2f} {y2_out:.2f} "
            f"L {x2_in:.2f} {y2_in:.2f} "
            f"A {r_in} {r_in} 0 0 0 {x1_in:.2f} {y1_in:.2f} Z"
        )
        paths.append(f'<path d="{d}" fill="{SDG_COLORS[i]}" />')
    return "\n".join(paths)

def render_sdg_badge():
    wheel_paths = generate_sdg_wheel_svg(cx=60, cy=60, r_in=30, r_out=54)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    margin: 0;
    padding: 15px;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 920px;
    height: 920px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }}
  
  .circle-badge {{
    width: 890px;
    height: 890px;
    border-radius: 50%;
    background: radial-gradient(circle at 50% 35%, #1E3A8A 0%, #152C70 65%, #0B1947 100%);
    border: 10px solid #FFFFFF;
    box-shadow: 0 16px 45px rgba(15, 23, 42, 0.40);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 35px 30px;
    text-align: center;
    color: #FFFFFF;
    position: relative;
    overflow: hidden;
  }}
  
  .header-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    margin-top: 5px;
    margin-bottom: 4px;
  }}
  .wheel-svg {{
    width: 80px;
    height: 80px;
    filter: drop-shadow(0 3px 6px rgba(0,0,0,0.30));
  }}
  .top-heading {{
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FFFFFF;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}
  .sub-heading {{
    font-size: 20px;
    font-weight: 600;
    color: #93C5FD;
    margin-bottom: 22px;
    letter-spacing: 0.8px;
  }}
  
  .sdg-tiles {{
    display: flex;
    gap: 16px;
    justify-content: center;
    align-items: center;
    margin-bottom: 22px;
  }}
  .sdg-tile {{
    width: 222px;
    height: 222px;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 16px;
    color: white;
    text-align: left;
    box-shadow: 0 8px 24px rgba(0,0,0,0.30);
    border: 2px solid rgba(255,255,255,0.45);
    position: relative;
  }}
  .sdg-9 {{ background: #F36D25; }}
  .sdg-12 {{ background: #CF8D2A; }}
  .sdg-13 {{ background: #48773E; }}
  
  .tile-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }}
  .tile-num {{
    font-size: 48px;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -1px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }}
  .tile-icon-svg {{
    width: 56px;
    height: 56px;
    fill: #FFFFFF;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
  }}
  .tile-title {{
    font-size: 15.5px;
    font-weight: 800;
    line-height: 1.25;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    text-shadow: 0 1px 3px rgba(0,0,0,0.3);
  }}
  
  .relevance-box {{
    background: rgba(255, 255, 255, 0.12);
    border: 1.5px solid rgba(255, 255, 255, 0.30);
    border-radius: 14px;
    padding: 14px 26px;
    max-width: 710px;
    font-size: 17px;
    line-height: 1.45;
    color: #F8FAFC;
    box-shadow: 0 4px 12px rgba(0,0,0,0.20);
    backdrop-filter: blur(8px);
  }}
  .relevance-highlight {{
    font-weight: 800;
    color: #38BDF8;
  }}
</style>
</head>
<body>

<div class='circle-badge'>
  <!-- Official 17-Color UN SDG Wheel & Header -->
  <div class='header-wrap'>
    <svg class='wheel-svg' viewBox='0 0 120 120'>
      {wheel_paths}
      <circle cx='60' cy='60' r='24' fill='#FFFFFF'/>
      <text x='60' y='65' text-anchor='middle' font-size='13' font-weight='900' fill='#1E3A8A' font-family='sans-serif'>SDGs</text>
    </svg>
    <div class='top-heading'>UN SDG ALIGNED</div>
  </div>
  
  <div class='sub-heading'>Key Sustainable Development Contributions</div>

  <div class='sdg-tiles'>
    <!-- SDG 9 TILE -->
    <div class='sdg-tile sdg-9'>
      <div class='tile-header'>
        <span class='tile-num'>9</span>
        <svg class='tile-icon-svg' viewBox='0 0 24 24'>
          <!-- Official Industry / Infrastructure / Innovation Cog & Factory -->
          <path d='M19 8h-1V3H6v5H5c-1.1 0-2 .9-2 2v11h18V10c0-1.1-.9-2-2-2zM8 5h8v3H8V5zm11 14H5v-7h14v7z'/>
          <rect x='7' y='14' width='2.5' height='3.5' rx='0.5'/>
          <rect x='11' y='14' width='2.5' height='3.5' rx='0.5'/>
          <rect x='15' y='14' width='2.5' height='3.5' rx='0.5'/>
        </svg>
      </div>
      <div class='tile-title'>Industry, Innovation &amp; Infrastructure</div>
    </div>

    <!-- SDG 12 TILE -->
    <div class='sdg-tile sdg-12'>
      <div class='tile-header'>
        <span class='tile-num'>12</span>
        <svg class='tile-icon-svg' viewBox='0 0 24 24'>
          <!-- Official Circular Economy Infinity Loop -->
          <path d='M18.5 6C16.01 6 13.9 7.67 13.12 10H10.88C10.1 7.67 7.99 6 5.5 6 2.46 6 0 8.46 0 11.5S2.46 17 5.5 17c2.49 0 4.6-1.67 5.38-4h2.24c.78 2.33 2.89 4 5.38 4 3.04 0 5.5-2.46 5.5-5.5S21.54 6 18.5 6zm-13 8.5C3.85 14.5 2.5 13.15 2.5 11.5S3.85 8.5 5.5 8.5c1.86 0 3.37 1.34 3.73 3.12L8.5 11.5l.73-.12C8.87 9.6 7.36 8.5 5.5 8.5zm13 0c-1.86 0-3.37-1.34-3.73-3.12l.73-.12-.73.12c.36 1.78 1.87 3.12 3.73 3.12 1.65 0 3-1.35 3-3s-1.35-3-3-3c-1.86 0-3.37 1.34-3.73 3.12l-.73-.12.73.12c.36 1.78 1.87 3.12 3.73 3.12z'/>
        </svg>
      </div>
      <div class='tile-title'>Responsible Consumption &amp; Production</div>
    </div>

    <!-- SDG 13 TILE -->
    <div class='sdg-tile sdg-13'>
      <div class='tile-header'>
        <span class='tile-num'>13</span>
        <svg class='tile-icon-svg' viewBox='0 0 24 24'>
          <!-- Official Climate Action Globe / Eye -->
          <path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z'/>
        </svg>
      </div>
      <div class='tile-title'>Climate<br>Action</div>
    </div>
  </div>

  <div class='relevance-box'>
    <span class='relevance-highlight'>Impact:</span> Resilient maritime bulk supply chains, zero vessel dead-freight waste, and <span class='relevance-highlight'>11.8% voyage fuel decarbonization</span> (IMO 2030).
  </div>
</div>

</body>
</html>
"""

    out_path = r"c:\vs studio\freight-forecast\sdg_central_badge.png"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 920, "height": 920}, device_scale_factor=2)
        page.set_content(html_content)
        page.screenshot(path=out_path, omit_background=True)
        browser.close()
    print(f"Rendered official SDG central badge to: {out_path}")

if __name__ == "__main__":
    render_sdg_badge()
