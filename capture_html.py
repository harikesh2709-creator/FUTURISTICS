import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 2760, "height": 1000}, device_scale_factor=2)
        
        file_path = f"file:///{os.path.abspath('architecture.html').replace(chr(92), '/')}"
        await page.goto(file_path)
        
        # Give it a second to load fonts
        await page.wait_for_timeout(2000)
        
        assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
        os.makedirs(assets_dir, exist_ok=True)
        
        out_path_slide = os.path.join(assets_dir, 'system_architecture_hd.png')
        out_path_4k = os.path.join(assets_dir, 'spectra_high_definition_architecture_4k.png')
        
        await page.screenshot(path=out_path_4k)
        
        # For the slide version, we can just save it identically since PPTX handles scaling.
        await page.screenshot(path=out_path_slide)
        
        await browser.close()
        print("Captured stunning HTML architecture diagram to PNG.")

if __name__ == "__main__":
    asyncio.run(main())
