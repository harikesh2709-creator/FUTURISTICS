import os
import sys
import asyncio
import subprocess
import time
import imageio_ffmpeg
import edge_tts
from playwright.sync_api import sync_playwright

VOICE = "en-IN-PrabhatNeural"  # Authentic 21-year-old Indian male student presenter voice
OUTPUT_DIR = r"c:\vs studio\freight-forecast"
RECORDINGS_DIR = os.path.join(OUTPUT_DIR, "video_recordings_new")
FINAL_MP4 = os.path.join(OUTPUT_DIR, "FreightForecast_Pro_New_Demo_1440p.mp4")

# 5 Natural, Engaging Narration Scripts by a 21-year-old Indian Male College Student for SIH
SCRIPTS = [
    # Segment 1: Intro + Live Demo Module 1 AI Rate Forecasting
    (
        "new_seg1_forecast.mp3",
        "Hello everyone! Respected judges and mentors, we are Team FUTURISTICS, and welcome to our demonstration of FreightForecast Pro. "
        "Let's jump straight into the heart of our platform—our live AI Rate Forecasting console. "
        "Here in Module 1, port authorities and chartering teams get instantaneous access to live spot fixtures and ninety-day predictive curves. "
        "Look at this: when we select the Capesize vessel class carrying one hundred and fifty thousand tons of Australian coking coal, "
        "our Holt-Winters algorithm instantly forecasts a seasonal rate softening from twenty-nine thousand one hundred dollars down to twenty-seven thousand seven hundred dollars per day. "
        "Now, take a look over at the right side at our proprietary Market Entry Score. With a current score of seventy out of one hundred, "
        "our engine triggers a favorable procurement signal, advising charterers to lock in forward Contract of Affreightment fixtures right now "
        "before cyclical freight spikes hit, protecting our procurement budget from spot market volatility."
    ),
    # Segment 2: Live Demo Module 2 Satellite AIS Telematics & GIS
    (
        "new_seg2_telematics.mp3",
        "Next, let's switch over to Module 2—our Real-Time Satellite AIS Fleet Telematics and Port Congestion GIS console. "
        "Right here on this interactive spatial map, we are continuously tracking commercial dry bulk carriers heading directly to the East Coast of India. "
        "When we click on active Capesize vessels like MV Ocean Titan or MV Bharat Victoria, you can see live telemetry right away: "
        "satellite-reported speed of thirteen point seven knots, route origin at Newcastle, destination Krishnapatnam, and ninety-eight percent voyage progress. "
        "Even more importantly, our telematics engine tracks anchorage queue congestion at Haldia and Paradip. "
        "The moment vessel bunching exceeds laytime thresholds, our system calculates demurrage accumulation risks, "
        "alerting port managers to divert to alternative deep-water berths before heavy twenty-two thousand dollar daily penalties start ticking."
    ),
    # Segment 3: Live Demo Module 3 & 4 Draught Solver & Hedging Advisor
    (
        "new_seg3_solver.mp3",
        "Moving on to Module 3, this is our Dynamic Vessel Draught and Berth Optimization solver. "
        "Riverine ports like Haldia face heavy siltation where shallow sandbars restrict arrival draught. "
        "Our engine cross-references chartered vessel dimensions against hourly astronomical tide curves. "
        "By dynamically optimizing parcel intake, our platform completely eliminates grounding risks and dead-freight penalties. "
        "Now in Module 4, our Contract Strategy Advisor performs automated spot-versus-forward hedging. "
        "When we input annual voyage requirements, the solver compares spot chartering against three-month and twelve-month Contracts of Affreightment. "
        "By locking in forward coverage at bottom-cycle rates, we achieve a simulated twenty-four point eight Crore rupee saving "
        "on a ten-million-ton imported coal program."
    ),
    # Segment 4: Mathematical Foundation & Architecture & Problem Context
    (
        "new_seg4_arch.mp3",
        "Now, let's look at the underlying technology and the critical national problem we are tackling. "
        "India imports over one hundred and fifty million metric tons of dry bulk cargo every single year, but the lack of predictive chartering intelligence leads to over six thousand Crore rupees lost annually. "
        "Our architecture tackles this head-on. At the ingestion layer, we harmonize five years of daily Baltic Exchange fixture indices "
        "with official Port Trust bathymetric circulars and real-time satellite AIS telemetry. "
        "Our core AI engine runs Triple Exponential Smoothing with multiplicative Holt-Winters decomposition. "
        "By separating macro commodity trends, cyclical trade demand, and Bay of Bengal monsoon seasonality, our model achieves "
        "an exceptional forecast accuracy with a validated Mean Absolute Percentage Error of just one point seven percent."
    ),
    # Segment 5: Feasibility, Quantifiable ROI & National Strategic Impact
    (
        "new_seg5_roi.mp3",
        "Finally, let's look at the feasibility, quantifiable ROI, and national impact. "
        "FreightForecast Pro is completely cloud-native, delivering sub-thirty-five millisecond query latency with Redis in-memory caching. "
        "It requires zero hardware installation on vessels and integrates directly with enterprise SAP and Oracle ERP systems. "
        "The financial impact is massive: a fourteen point two to eighteen point five percent cut in net freight costs, "
        "saving fifteen to thirty thousand dollars per day in eliminated demurrage, with a payback period under twenty-two days. "
        "Plus, weather-optimized speed curves reduce voyage fuel consumption by eleven point eight percent, supporting IMO 2030 green shipping goals. "
        "FreightForecast Pro delivers actionable maritime intelligence for an Atmanirbhar Bharat. Thank you so much from Team FUTURISTICS!"
    )
]

def get_media_duration(file_path):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg_exe, "-i", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    import re
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        hours, mins, secs = match.groups()
        return float(hours) * 3600 + float(mins) * 60 + float(secs)
    return 0.0

async def generate_all_audio():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    audio_files = []
    durations = []
    print("=" * 60)
    print("Generating Indian Male Voiceover (21yo College Student / SIH Style)...")
    print("=" * 60)
    for fname, text in SCRIPTS:
        out_path = os.path.join(RECORDINGS_DIR, fname)
        if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
            print(f"Synthesizing: {fname}...")
            comm = edge_tts.Communicate(text, VOICE, rate="+4%", pitch="+2Hz")
            await comm.save(out_path)
        dur = get_media_duration(out_path)
        audio_files.append(out_path)
        durations.append(dur)
        print(f"Audio: {fname} | Duration: {dur:.2f}s")
    
    master_audio = os.path.join(RECORDINGS_DIR, "full_voiceover_new.mp3")
    concat_list = os.path.join(RECORDINGS_DIR, "audio_concat.txt")
    if not os.path.exists(master_audio) or os.path.getsize(master_audio) < 1000:
        with open(concat_list, "w") as f:
            for af in audio_files:
                f.write(f"file '{af.replace('\\\\', '/')}'\n")
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", master_audio]
        subprocess.run(cmd, check=True)
        
    total_audio_dur = get_media_duration(master_audio)
    print(f"Master voiceover ready: {master_audio} | Duration: {total_audio_dur:.2f}s")
    return master_audio, durations

def record_synchronized_walkthrough(durations):
    print("=" * 60)
    print("Starting 1440p Playwright Screen Recording (Prioritizing Main Demo)...")
    print("=" * 60)
    
    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--force-color-profile=srgb"]
        )
        context = browser.new_context(
            viewport={"width": 2560, "height": 1440},
            device_scale_factor=1,
            record_video_dir=RECORDINGS_DIR,
            record_video_size={"width": 2560, "height": 1440}
        )
        page = context.new_page()
        page.set_default_timeout(30000)
        
        # Start at local server
        page.goto("http://127.0.0.1:8765/", wait_until="networkidle")
        page.wait_for_timeout(2000)
        
        # -------------------------------------------------------------
        # SEGMENT 1: Intro + Live Demo Module 1 (Forecast)
        # -------------------------------------------------------------
        print(f"[Segment 1] Recording Rate Forecasting Console (target: {durations[0]:.1f}s)...")
        seg1_start = time.time()
        
        # Ensure we are on forecast panel
        page.click("#nav-forecast")
        page.wait_for_timeout(2000)
        
        # Toggle vessel class dropdown: Panamax
        vessel_select = page.locator("#forecastVesselSelect")
        if vessel_select.count() > 0:
            vessel_select.select_option("PANAMAX")
            page.wait_for_timeout(1500)
            page.click("#runForecastBtn")
            page.wait_for_timeout(4000)
            
            # Toggle vessel class dropdown: Supramax
            vessel_select.select_option("SUPRAMAX")
            page.wait_for_timeout(1500)
            page.click("#runForecastBtn")
            page.wait_for_timeout(4000)
            
            # Toggle vessel class back to Capesize
            vessel_select.select_option("CAPESIZE")
            page.wait_for_timeout(1500)
            page.click("#runForecastBtn")
            page.wait_for_timeout(4000)
            
            # Toggle forecast horizon: 180 Days
            horizon_select = page.locator("#forecastHorizonSelect")
            horizon_select.select_option("180")
            page.wait_for_timeout(2000)
            page.click("#runForecastBtn")
            page.wait_for_timeout(4000)
            
            horizon_select.select_option("90")
            page.wait_for_timeout(1500)
            page.click("#runForecastBtn")
            page.wait_for_timeout(3000)
        
        # Hover over main forecast chart points
        chart_box = page.locator("#mainForecastChart")
        if chart_box.count() > 0:
            box = chart_box.bounding_box()
            if box:
                for frac in [0.2, 0.4, 0.6, 0.8]:
                    page.mouse.move(box["x"] + box["width"] * frac, box["y"] + box["height"] * 0.5)
                    page.wait_for_timeout(1500)
                    
        # Highlight Market Entry Score card
        market_entry = page.locator("#marketEntryContent")
        if market_entry.count() > 0:
            market_entry.hover()
            page.wait_for_timeout(4000)
            
        elapsed = time.time() - seg1_start
        if elapsed < durations[0]:
            page.wait_for_timeout(int((durations[0] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 2: Live Demo — Module 2 Satellite AIS Telematics & GIS
        # -------------------------------------------------------------
        print(f"[Segment 2] Recording Satellite AIS Fleet Telematics (target: {durations[1]:.1f}s)...")
        seg2_start = time.time()
        
        page.click("[data-panel='telematics']")
        page.wait_for_timeout(3000)
        
        cape_btn = page.locator("#telematics-class-filters button[data-class='Capesize']")
        if cape_btn.count() > 0:
            cape_btn.click()
            page.wait_for_timeout(3500)
            
        panamax_btn = page.locator("#telematics-class-filters button[data-class='Panamax']")
        if panamax_btn.count() > 0:
            panamax_btn.click()
            page.wait_for_timeout(3500)
            
        all_btn = page.locator("#telematics-class-filters button[data-class='ALL']")
        if all_btn.count() > 0:
            all_btn.click()
            page.wait_for_timeout(3500)
            
        vessel_cards = page.locator("#telematics-feed > div")
        try:
            card_count = vessel_cards.count()
            if card_count > 0:
                for i in range(min(card_count, 3)):
                    try:
                        vessel_cards.nth(i).hover(force=True, timeout=3000)
                        vessel_cards.nth(i).click(force=True, timeout=3000)
                    except Exception as e:
                        print(f"Skipping card {i} hover due to error: {e}")
                    page.wait_for_timeout(4000)
        except Exception as e:
            print(f"Skipping vessel cards loop due to: {e}")
                
        map_elem = page.locator("#map-container")
        if map_elem.count() > 0:
            mbox = map_elem.bounding_box()
            if mbox:
                page.mouse.move(mbox["x"] + mbox["width"] * 0.5, mbox["y"] + mbox["height"] * 0.5)
                page.mouse.wheel(0, -300)  # zoom in
                page.wait_for_timeout(3000)
                page.mouse.wheel(0, 300)   # zoom out
                page.wait_for_timeout(3000)
                
        elapsed = time.time() - seg2_start
        if elapsed < durations[1]:
            page.wait_for_timeout(int((durations[1] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 3: Live Demo — Module 3 & 4 Draught Solver & Hedging
        # -------------------------------------------------------------
        print(f"[Segment 3] Recording Vessel Optimizer & Contract Hedging (target: {durations[2]:.1f}s)...")
        seg3_start = time.time()
        
        page.click("#nav-vessel")
        page.wait_for_timeout(2500)
        
        cargo_input = page.locator("#vesselCargoInput")
        if cargo_input.count() > 0:
            cargo_input.fill("120000")
            page.wait_for_timeout(1500)
            page.click("#optimizeVesselBtn")
            page.wait_for_timeout(5000)
            
        page.click("#nav-port")
        page.wait_for_timeout(2500)
        page.evaluate("window.scrollBy({top: 300, behavior: 'smooth'})")
        page.wait_for_timeout(3000)
        page.evaluate("window.scrollBy({top: -300, behavior: 'smooth'})")
        page.wait_for_timeout(2000)
        
        page.click("[data-panel='contract']")
        page.wait_for_timeout(2500)
        
        analyze_btn = page.locator("#analyzeContractBtn")
        if analyze_btn.count() > 0:
            analyze_btn.click()
            page.wait_for_timeout(5000)
            
        page.evaluate("window.scrollBy({top: 400, behavior: 'smooth'})")
        page.wait_for_timeout(4000)
        page.evaluate("window.scrollBy({top: -400, behavior: 'smooth'})")
        page.wait_for_timeout(3000)
        
        elapsed = time.time() - seg3_start
        if elapsed < durations[2]:
            page.wait_for_timeout(int((durations[2] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 4: Math Arch & Problem context
        # -------------------------------------------------------------
        print(f"[Segment 4] Recording Architecture & Formulation (target: {durations[3]:.1f}s)...")
        seg4_start = time.time()
        
        # Navigate back to main forecast panel to see the charts
        page.click("#nav-forecast", force=True)
        page.wait_for_timeout(2000)
        
        # Scroll up to the header metrics to show context
        page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        page.wait_for_timeout(3000)
        
        # Hover over KPI badges
        kpi_bar = page.locator("#kpiBar")
        if kpi_bar.count() > 0:
            kpi_bar.hover(force=True, timeout=3000)
            page.wait_for_timeout(3000)
            
        # Scroll to seasonal decomposition charts
        page.evaluate("window.scrollBy({top: 600, behavior: 'smooth'})")
        page.wait_for_timeout(4000)
        
        trend_canvas = page.locator("#decompTrendChart")
        if trend_canvas.count() > 0:
            try:
                trend_canvas.hover(force=True, timeout=3000)
            except Exception:
                pass
            page.wait_for_timeout(4000)
            
        seasonal_canvas = page.locator("#decompSeasonalChart")
        if seasonal_canvas.count() > 0:
            try:
                seasonal_canvas.hover(force=True, timeout=3000)
            except Exception:
                pass
            page.wait_for_timeout(4000)
            
        acc_box = page.locator("#accuracyMetrics")
        if acc_box.count() > 0:
            acc_box.hover()
            page.wait_for_timeout(5000)
            
        page.evaluate("window.scrollBy({top: -600, behavior: 'smooth'})")
        page.wait_for_timeout(3000)
        
        elapsed = time.time() - seg4_start
        if elapsed < durations[3]:
            page.wait_for_timeout(int((durations[3] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 5: Feasibility, Quantifiable ROI & Impact
        # -------------------------------------------------------------
        print(f"[Segment 5] Recording Risk Console & Impact Summary (target: {durations[4]:.1f}s)...")
        seg5_start = time.time()
        
        page.click("[data-panel='risk']")
        page.wait_for_timeout(3500)
        
        alerts_list = page.locator("#riskAlertsList")
        if alerts_list.count() > 0:
            try:
                alerts_list.hover(force=True, timeout=3000)
            except Exception:
                pass
            page.wait_for_timeout(3500)
            
        vol_chart = page.locator("#volatilityChart")
        if vol_chart.count() > 0:
            try:
                vol_chart.hover(force=True, timeout=3000)
            except Exception:
                pass
            page.wait_for_timeout(3500)
            
        page.click("[data-panel='ai']")
        page.wait_for_timeout(2500)
        
        first_prompt = page.locator("#ai-suggested-prompts span").first
        if first_prompt.count() > 0:
            first_prompt.click()
            page.wait_for_timeout(5000)
            
        page.click("#nav-forecast")
        page.wait_for_timeout(2000)
        page.mouse.move(1280, 200)
        page.wait_for_timeout(4000)
        
        elapsed = time.time() - seg5_start
        if elapsed < durations[4]:
            page.wait_for_timeout(int((durations[4] - elapsed) * 1000) + 1000)
            
        video_path = page.video.path()
        context.close()
        browser.close()
        time.sleep(2)
        
    print(f"Playwright finished recording raw WebM video to: {video_path}")
    return video_path

def mux_final_mp4(webm_video, master_audio):
    print("=" * 60)
    print("Muxing 1440p Video & Audio into Broadcast MP4...")
    print("=" * 60)
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", webm_video,
        "-i", master_audio,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_MP4
    ]
    
    subprocess.run(cmd, check=True)
    
    size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    duration = get_media_duration(FINAL_MP4)
    print(f"\n[SUCCESS] Final 1440p Video Generated: {FINAL_MP4}")
    print(f"File Size:  {size_mb:.2f} MB")
    print("=" * 60)

def main():
    master_audio, durations = asyncio.run(generate_all_audio())
    webm_video = record_synchronized_walkthrough(durations)
    mux_final_mp4(webm_video, master_audio)

if __name__ == "__main__":
    main()
