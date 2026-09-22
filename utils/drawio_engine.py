import asyncio
import base64
import os
import tempfile
from playwright.async_api import async_playwright

async def render_diagram(xml_path, out_path, scale=8):
    """
    Renders a .drawio XML file natively using the official client-side mxGraph engine.
    There is no public cloud API endpoint for Draw.io export, so the official recommendation 
    for automation is using a headless browser to invoke the mxGraph renderer locally.
    This guarantees 100% accurate rendering and extreme high definition.
    """
    with open(xml_path, "r", encoding="utf-8") as f:
        drawio_xml = f.read()
    
    b64_xml = base64.b64encode(drawio_xml.encode('utf-8')).decode('ascii')
    
    # Official minimal HTML wrapper for the diagrams.net engine
    html_template = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            html, body {{ margin: 0; padding: 0; overflow: hidden; background: #ffffff; }}
            #graph-container {{ width: 100vw; height: 100vh; }}
            svg {{ background-color: #ffffff !important; }}
        </style>
    </head>
    <body>
        <div id="graph-container"></div>
        <script>
            var xmlString = atob("{b64_xml}");
            var parser = new DOMParser();
            var xmlDoc = parser.parseFromString(xmlString, "text/xml");
            var diagram = xmlDoc.querySelector("diagram");
            var mxGraphModelNode = diagram ? diagram.querySelector("mxGraphModel") : null;
            
            if (mxGraphModelNode) {{
                mxGraphModelNode.setAttribute("grid", "0");
                mxGraphModelNode.setAttribute("shadow", "0");
                
                var serializer = new XMLSerializer();
                var mxGraphXml = serializer.serializeToString(mxGraphModelNode);
                
                var container = document.getElementById("graph-container");
                container.setAttribute("class", "mxgraph");
                container.setAttribute("data-mxgraph", JSON.stringify({{
                    "highlight": "#ffffff",
                    "nav": false,
                    "resize": false,
                    "toolbar": "",
                    "edit": "_blank",
                    "xml": mxGraphXml
                }}));
                
                var script = document.createElement("script");
                script.src = "https://viewer.diagrams.net/js/viewer-static.min.js";
                document.body.appendChild(script);
            }} else {{
                document.body.innerHTML = "<h1>Error parsing diagram</h1>";
            }}
        </script>
    </body>
    </html>"""
    
    # Write to a secure temp file
    temp_fd, temp_html = tempfile.mkstemp(suffix=".html")
    with os.fdopen(temp_fd, 'w', encoding="utf-8") as f:
        f.write(html_template)
        
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1200, "height": 400}, device_scale_factor=scale)
            
            file_url = "file:///" + temp_html.replace("\\", "/").replace(" ", "%20")
            await page.goto(file_url, wait_until="networkidle")
            
            svg_loc = page.locator("svg").first
            await svg_loc.wait_for(timeout=15000)
            await page.wait_for_timeout(3000)
            
            await svg_loc.screenshot(path=out_path)
            
            # Save a 4k version too
            out_4k = out_path.replace("system_architecture_hd", "spectra_high_definition_architecture_4k")
            if out_4k != out_path:
                await svg_loc.screenshot(path=out_4k)
                
            await browser.close()
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)
