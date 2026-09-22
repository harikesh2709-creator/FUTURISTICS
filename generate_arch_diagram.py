import asyncio
from playwright.async_api import async_playwright
import os

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Architecture</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            padding: 40px;
            background-color: transparent;
            font-family: 'Inter', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 1400px;
            height: 600px;
        }

        .container {
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 20px;
            padding: 30px;
            box-sizing: border-box;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            position: relative;
            display: flex;
            flex-direction: column;
            border: 2px solid #cbd5e1;
        }

        .layer-title {
            font-size: 20px;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        .flex-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
            flex: 1;
            width: 100%;
        }

        .column {
            display: flex;
            flex-direction: column;
            gap: 20px;
            flex: 1;
            height: 100%;
        }

        .box {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 2px solid #e2e8f0;
            position: relative;
            z-index: 2;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: transform 0.3s ease;
        }

        .box-title {
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
        }

        .box-subtitle {
            font-size: 16px;
            color: #64748b;
            font-weight: 600;
        }

        /* Specific Colors */
        .ui-box { border-left: 8px solid #3b82f6; }
        .api-box { border-left: 8px solid #10b981; }
        .engine-box { border-left: 8px solid #8b5cf6; }
        .data-box { border-left: 8px solid #f59e0b; }
        .ext-box { border-left: 8px solid #ef4444; }

        /* Arrows Container */
        svg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none;
        }

        .section-wrap {
            background: rgba(255, 255, 255, 0.5);
            border: 2px dashed #94a3b8;
            border-radius: 16px;
            padding: 20px;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
        }

        .tech-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin-top: 12px;
        }
        
        .tag {
            background: #f1f5f9;
            color: #334155;
            font-size: 14px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid #cbd5e1;
        }
    </style>
</head>
<body>

    <div class="container" id="arch-container">
        
        <svg id="arrows-svg">
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#64748b" />
                </marker>
                <marker id="arrowhead-bi" markerWidth="10" markerHeight="7" refX="1" refY="3.5" orient="auto-start-reverse">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#64748b" />
                </marker>
            </defs>
            <!-- Arrows will be drawn here dynamically -->
        </svg>

        <div class="flex-row">
            
            <!-- External Data Sources -->
            <div class="column" style="flex: 0.8">
                <div class="section-wrap" id="sec-ext">
                    <div class="layer-title">External Data Inputs</div>
                    <div class="box ext-box" id="node-market" style="flex: 1; margin-bottom: 15px;">
                        <div class="box-title">Global Markets</div>
                        <div class="box-subtitle">Baltic Exchange Indices</div>
                    </div>
                    <div class="box ext-box" id="node-vessel" style="flex: 1; margin-bottom: 15px;">
                        <div class="box-title">Fleet Telemetry</div>
                        <div class="box-subtitle">Satellite AIS & Copernicus Weather</div>
                    </div>
                    <div class="box ext-box" id="node-port" style="flex: 1;">
                        <div class="box-title">Port Gazette</div>
                        <div class="box-subtitle">Tidal Tables & Draft Circulars</div>
                    </div>
                </div>
            </div>

            <!-- Backend & Analytics -->
            <div class="column" style="flex: 1.2">
                <div class="section-wrap" id="sec-backend">
                    <div class="layer-title">Core Processing Engine</div>
                    <div class="box api-box" id="node-api">
                        <div class="box-title">FastAPI Microservice</div>
                        <div class="box-subtitle">Asynchronous REST API</div>
                        <div class="tech-tags">
                            <span class="tag">Python</span>
                            <span class="tag">Uvicorn</span>
                            <span class="tag">Docker</span>
                        </div>
                    </div>
                    
                    <div class="box engine-box" id="node-engine" style="margin-top: auto; margin-bottom: auto;">
                        <div class="box-title">Mathematical Analytics Core</div>
                        <div class="box-subtitle">Holt-Winters & Monte Carlo Simulation</div>
                        <div class="tech-tags">
                            <span class="tag">NumPy</span>
                            <span class="tag">SciPy</span>
                            <span class="tag">Statsmodels</span>
                        </div>
                    </div>

                    <div class="flex-row" style="margin-top: auto;">
                        <div class="box data-box" id="node-cache" style="flex: 1;">
                            <div class="box-title">In-Memory Cache</div>
                            <div class="box-subtitle">Sub-35ms Latency</div>
                            <div class="tech-tags"><span class="tag">Redis</span></div>
                        </div>
                        <div class="box data-box" id="node-db" style="flex: 1;">
                            <div class="box-title">Spatial Database</div>
                            <div class="box-subtitle">Port Parameters</div>
                            <div class="tech-tags"><span class="tag">PostgreSQL/PostGIS</span></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Frontend -->
            <div class="column" style="flex: 1">
                <div class="section-wrap" id="sec-ui">
                    <div class="layer-title">Client Presentation Layer</div>
                    
                    <div class="box ui-box" id="node-ui" style="flex: 1; margin-bottom: 15px;">
                        <div class="box-title">Executive Dashboard</div>
                        <div class="box-subtitle">Interactive Glassmorphic UI</div>
                        <div class="tech-tags">
                            <span class="tag">React.js</span>
                            <span class="tag">Tailwind CSS</span>
                        </div>
                    </div>

                    <div class="box ui-box" id="node-maps" style="flex: 1;">
                        <div class="box-title">Nautical GIS & Charts</div>
                        <div class="box-subtitle">Live Vessel Tracking & Rate Trends</div>
                        <div class="tech-tags">
                            <span class="tag">Leaflet.js</span>
                            <span class="tag">Chart.js</span>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </div>

    <script>
        function drawArrow(id1, id2, bi=false) {
            const el1 = document.getElementById(id1);
            const el2 = document.getElementById(id2);
            const container = document.getElementById('arch-container');
            const svg = document.getElementById('arrows-svg');
            
            const rect1 = el1.getBoundingClientRect();
            const rect2 = el2.getBoundingClientRect();
            const cRect = container.getBoundingClientRect();

            const x1 = rect1.right - cRect.left;
            const y1 = rect1.top + (rect1.height/2) - cRect.top;
            
            const x2 = rect2.left - cRect.left;
            const y2 = rect2.top + (rect2.height/2) - cRect.top;

            // Simple bezier curve for smooth arrows
            const midX = (x1 + x2) / 2;
            const pathData = `M ${x1} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${x2} ${y2}`;

            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('d', pathData);
            path.setAttribute('fill', 'none');
            path.setAttribute('stroke', '#94a3b8');
            path.setAttribute('stroke-width', '4');
            path.setAttribute('stroke-dasharray', '8,4');
            
            if (bi) {
                path.setAttribute('marker-start', 'url(#arrowhead-bi)');
            }
            path.setAttribute('marker-end', 'url(#arrowhead)');

            svg.appendChild(path);
        }
        
        function drawVerticalArrow(id1, id2, bi=false) {
            const el1 = document.getElementById(id1);
            const el2 = document.getElementById(id2);
            const container = document.getElementById('arch-container');
            const svg = document.getElementById('arrows-svg');
            
            const rect1 = el1.getBoundingClientRect();
            const rect2 = el2.getBoundingClientRect();
            const cRect = container.getBoundingClientRect();

            const x1 = rect1.left + (rect1.width/2) - cRect.left;
            const y1 = rect1.bottom - cRect.top;
            
            const x2 = rect2.left + (rect2.width/2) - cRect.left;
            const y2 = rect2.top - cRect.top;

            const pathData = `M ${x1} ${y1} L ${x2} ${y2}`;

            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('d', pathData);
            path.setAttribute('fill', 'none');
            path.setAttribute('stroke', '#94a3b8');
            path.setAttribute('stroke-width', '4');
            
            if (bi) {
                path.setAttribute('marker-start', 'url(#arrowhead-bi)');
            }
            path.setAttribute('marker-end', 'url(#arrowhead)');

            svg.appendChild(path);
        }

        window.onload = () => {
            // Data to API
            drawArrow('node-market', 'node-api');
            drawArrow('node-vessel', 'node-api');
            drawArrow('node-port', 'node-api');

            // API to Engine
            drawVerticalArrow('node-api', 'node-engine', true);
            
            // Engine to Cache/DB
            drawVerticalArrow('node-engine', 'node-cache', true);
            drawVerticalArrow('node-engine', 'node-db', true);

            // API to UI
            drawArrow('node-api', 'node-ui', true);
            
            // UI to Maps
            drawVerticalArrow('node-ui', 'node-maps');
        };
    </script>
</body>
</html>
"""

async def generate():
    output_png = r"c:\vs studio\freight-forecast\system_architecture_diagram_new.png"
    
    html_file = "temp_arch.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            viewport={"width": 1450, "height": 650},
            device_scale_factor=2.0  # High DPI for crisp PPT image
        )
        
        file_url = f"file:///{os.path.abspath(html_file).replace(chr(92), '/')}"
        await page.goto(file_url, wait_until="networkidle")
        
        # Wait a small moment to ensure the JS drawing the arrows finishes
        await asyncio.sleep(1.0)
        
        # Locate the container and screenshot it
        container = page.locator("#arch-container")
        await container.screenshot(path=output_png, type="png")
        
        await browser.close()
    
    # cleanup HTML
    if os.path.exists(html_file):
        os.remove(html_file)

    print(f"High-res Architecture diagram saved to {output_png}")

if __name__ == "__main__":
    asyncio.run(generate())
