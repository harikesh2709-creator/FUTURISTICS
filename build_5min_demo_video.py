"""
Generate 5-Minute High-Definition 1440p Video Walkthrough with Natural Male Voiceover
for FreightForecast Pro (Team FUTURISTICS - Smart India Hackathon 2026).
"""

import os
import sys
import asyncio
import subprocess
import time
import imageio_ffmpeg
import edge_tts
from playwright.sync_api import sync_playwright

VOICE = "en-US-ChristopherNeural"  # Professional, natural, authoritative male presenter voice
OUTPUT_DIR = r"c:\vs studio\freight-forecast"
RECORDINGS_DIR = os.path.join(OUTPUT_DIR, "video_recordings")
FINAL_MP4 = os.path.join(OUTPUT_DIR, "FreightForecast_Pro_5Min_Demo_1440p.mp4")

# 6 Detailed, Professional Narration Scripts (Timed to ~5 minutes total)
SCRIPTS = [
    # Segment 1: Introduction & National Maritime Problem (approx 48s)
    (
        "seg1_intro.mp3",
        "Greetings, respected judges and evaluators. We are Team FUTURISTICS, presenting FreightForecast Pro "
        "for Smart India Hackathon 2026, under Problem Statement ID SIH26006. "
        "India's core industries, including power utilities and steel manufacturers, import over one hundred and fifty "
        "million metric tons of dry bulk cargo and coking coal annually through East Coast ports like Paradip, Haldia, and Visakhapatnam. "
        "However, global shipping markets are notoriously volatile. Without predictive intelligence, chartering desks rely on "
        "reactive heuristics and static spreadsheets. This lack of foresight leads to massive demurrage penalties, inefficient vessel selection, "
        "and costly dead-freight—draining over six thousand Crore rupees annually across Indian ports. "
        "FreightForecast Pro transforms this paradigm through an intelligent, AI-powered maritime freight forecasting and berth-draught optimization hub."
    ),
    # Segment 2: Mathematical Architecture & Engineering Pillars (approx 48s)
    (
        "seg2_math_arch.mp3",
        "Our system architecture is founded on four high-performance engineering pillars. "
        "At the ingestion layer, we harmonize five years of daily Baltic Exchange fixture indices—Capesize BCI, Panamax BPI, "
        "and Supramax BSI—with official Port Trust bathymetric circulars and real-time satellite AIS vessel telemetry. "
        "Our core AI forecasting engine applies Triple Exponential Smoothing with multiplicative Holt-Winters decomposition. "
        "By isolating macro commodity trends, cyclical trade demand, and Bay of Bengal monsoon seasonality, our model achieves "
        "an exceptional forecast accuracy with a validated Mean Absolute Percentage Error of just one point seven percent. "
        "Simultaneously, our hydrodynamic engine dynamically validates Under-Keel Clearance, enforcing UKC greater than or equal to one point five meters "
        "against astronomical tides and siltation records, while a mixed-integer solver minimizes landed cost per metric ton."
    ),
    # Segment 3: Live Demo - Module 1: AI Rate Forecasting (approx 52s)
    (
        "seg3_forecasting.mp3",
        "Let us examine the live production dashboard running on our asynchronous Python FastAPI and React architecture. "
        "In Module 1, the AI Rate Forecasting console, users have instantaneous access to live spot fixtures and 90-day predictive curves. "
        "Selecting the Capesize vessel class carrying one hundred and fifty thousand tons of Australian coking coal, "
        "our Holt-Winters algorithm projects a seasonal rate softening from twenty-nine thousand one hundred dollars down to twenty-seven thousand seven hundred dollars per day. "
        "On the right, notice our proprietary Market Entry Score. With a current index of seventy out of one hundred, "
        "the engine issues a favorable procurement signal, advising chartering executives to lock in forward Contract of Affreightment fixtures "
        "before cyclical freight surges occur, insulating procurement budgets from spot market volatility."
    ),
    # Segment 4: Live Demo - Module 2: Satellite AIS Telematics & Congestion GIS (approx 55s)
    (
        "seg4_telematics.mp3",
        "Moving to Module 2, we access our Real-Time Satellite AIS Fleet Telematics and Port Congestion GIS console. "
        "Here, an interactive spatial map continuously monitors commercial dry bulk carriers inbound to the East Coast of India. "
        "Clicking on active Capesize vessels such as the MV Ocean Titan and MV Bharat Victoria, we inspect live telemetry: "
        "satellite-reported speed over ground at thirteen point seven knots, route origin at Newcastle, destination at Krishnapatnam, and a ninety-eight percent voyage progress status. "
        "Crucially, our telematics engine monitors anchorage queue densities at Haldia and Paradip. "
        "When vessel bunching threatens to exceed laytime thresholds, the system calculates demurrage accumulation risks, "
        "alerting logistics managers to reroute to alternative deep-water berths before punitive twenty-two thousand dollar daily penalties accrue."
    ),
    # Segment 5: Live Demo - Module 3 & 4: Vessel Draught Solver & Hedging Advisor (approx 52s)
    (
        "seg5_solver_hedge.mp3",
        "Next, Module 3 executes Dynamic Vessel Draught and Berth Optimization. "
        "Riverine ports like Haldia present severe siltation hazards where shallow sandbars restrict arrival draught. "
        "Our engine cross-references chartered vessel dimensions against hourly astronomical tide curves. "
        "By dynamically optimizing parcel intake, the system eliminates both ship grounding risks and dead-freight penalties. "
        "In Module 4, our Contract Strategy Advisor executes automated spot-versus-forward hedging. "
        "Entering annual voyage requirements, the solver compares Spot chartering against three-month and twelve-month Contracts of Affreightment. "
        "By locking forward coverage at bottom-cycle rates, the platform demonstrates a simulated twenty-four point eight Crore rupee saving "
        "on a ten-million-ton imported coal program."
    ),
    # Segment 6: Feasibility, Quantifiable ROI & National Strategic Impact (approx 45s)
    (
        "seg6_impact_roi.mp3",
        "From an operational and technical standpoint, FreightForecast Pro is fully cloud-native, delivering sub-thirty-five millisecond query latency "
        "via Redis in-memory caching. It requires zero hardware installation on vessels and integrates directly into enterprise SAP and Oracle ERP environments. "
        "The economic impact is transformative: a fourteen point two to eighteen point five percent reduction in net freight expenditure, "
        "saving fifteen to thirty thousand dollars per day in eliminated demurrage, with a full deployment payback period under twenty-two days. "
        "Furthermore, weather-optimized speed curves cut voyage fuel consumption by eleven point eight percent, aligning with IMO 2030 decarbonization goals. "
        "FreightForecast Pro delivers strategic maritime intelligence for a self-reliant India. Thank you from Team FUTURISTICS."
    )
]

def get_media_duration(file_path):
    """Get exact duration in seconds of media file using ffmpeg."""
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
    """Generate all speech segments using edge-tts (or reuse existing cached files)."""
    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    audio_files = []
    durations = []
    print("=" * 60)
    print("Checking / generating natural neural voiceover audio tracks...")
    print("=" * 60)
    for fname, text in SCRIPTS:
        out_path = os.path.join(RECORDINGS_DIR, fname)
        if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
            print(f"Synthesizing: {fname} ({len(text.split())} words)...")
            comm = edge_tts.Communicate(text, VOICE, rate="+2%", pitch="-1Hz")
            await comm.save(out_path)
        dur = get_media_duration(out_path)
        audio_files.append(out_path)
        durations.append(dur)
        print(f"Audio segment: {fname} | Duration: {dur:.2f}s")
    
    # Merge audio files into master full_voiceover.mp3
    master_audio = os.path.join(RECORDINGS_DIR, "full_voiceover.mp3")
    concat_list = os.path.join(RECORDINGS_DIR, "audio_concat.txt")
    if not os.path.exists(master_audio) or os.path.getsize(master_audio) < 1000:
        with open(concat_list, "w") as f:
            for af in audio_files:
                # Use forward slashes for ffmpeg concat
                f.write(f"file '{af.replace('\\\\', '/')}'\n")
                
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", master_audio]
        subprocess.run(cmd, check=True)
        
    total_audio_dur = get_media_duration(master_audio)
    print(f"Master voiceover ready: {master_audio} | Total Duration: {total_audio_dur:.2f}s ({total_audio_dur/60:.2f} mins)")
    return master_audio, durations

def record_synchronized_walkthrough(durations):
    """Drive Playwright browser through interactive features synchronized to audio segment durations."""
    print("=" * 60)
    print("Starting 1440p (2560x1440) Playwright Screen Recording...")
    print("=" * 60)
    
    os.makedirs(RECORDINGS_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--force-color-profile=srgb"
            ]
        )
        
        # 1440p Quad-HD resolution: 2560 x 1440
        context = browser.new_context(
            viewport={"width": 2560, "height": 1440},
            device_scale_factor=1,
            record_video_dir=RECORDINGS_DIR,
            record_video_size={"width": 2560, "height": 1440}
        )
        
        page = context.new_page()
        page.set_default_timeout(30000)
        
        # -------------------------------------------------------------
        # SEGMENT 1: Introduction & Problem Context (~48s)
        # -------------------------------------------------------------
        print(f"[Segment 1] Recording Introduction (target: {durations[0]:.1f}s)...")
        seg1_start = time.time()
        page.goto("http://127.0.0.1:8765/", wait_until="networkidle")
        page.wait_for_timeout(2000)
        
        # Scroll header and show dashboard overview
        page.mouse.move(1280, 400)
        page.wait_for_timeout(3000)
        
        # Hover over KPI badges
        kpi_bar = page.locator("#kpiBar")
        if kpi_bar.count() > 0:
            kpi_bar.hover()
            page.wait_for_timeout(3000)
            
        # Hover connection status
        conn_pill = page.locator("#connectionStatusPill")
        if conn_pill.count() > 0:
            conn_pill.hover()
            page.wait_for_timeout(2500)
            
        # Smooth scroll down to view cards
        page.evaluate("window.scrollBy({top: 350, behavior: 'smooth'})")
        page.wait_for_timeout(4000)
        page.evaluate("window.scrollBy({top: -350, behavior: 'smooth'})")
        page.wait_for_timeout(3000)
        
        # Fill remaining segment 1 time
        elapsed = time.time() - seg1_start
        if elapsed < durations[0]:
            page.wait_for_timeout(int((durations[0] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 2: Mathematical Foundation & Architecture (~48s)
        # -------------------------------------------------------------
        print(f"[Segment 2] Recording Architecture & Formulation (target: {durations[1]:.1f}s)...")
        seg2_start = time.time()
        
        # Scroll to seasonal decomposition charts
        page.evaluate("window.scrollBy({top: 600, behavior: 'smooth'})")
        page.wait_for_timeout(4000)
        
        # Hover over trend component chart
        trend_canvas = page.locator("#decompTrendChart")
        if trend_canvas.count() > 0:
            trend_canvas.hover()
            page.wait_for_timeout(4000)
            
        # Hover over seasonal component chart
        seasonal_canvas = page.locator("#decompSeasonalChart")
        if seasonal_canvas.count() > 0:
            seasonal_canvas.hover()
            page.wait_for_timeout(4000)
            
        # Hover over accuracy metrics box
        acc_box = page.locator("#accuracyMetrics")
        if acc_box.count() > 0:
            acc_box.hover()
            page.wait_for_timeout(5000)
            
        page.evaluate("window.scrollBy({top: -600, behavior: 'smooth'})")
        page.wait_for_timeout(3000)
        
        elapsed = time.time() - seg2_start
        if elapsed < durations[1]:
            page.wait_for_timeout(int((durations[1] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 3: Live Demo — Module 1 Rate Forecasting (~52s)
        # -------------------------------------------------------------
        print(f"[Segment 3] Recording Rate Forecasting Console (target: {durations[2]:.1f}s)...")
        seg3_start = time.time()
        
        # Ensure we are on forecast panel
        page.click("#nav-forecast")
        page.wait_for_timeout(2000)
        
        # Toggle vessel class dropdown: Panamax
        vessel_select = page.locator("#forecastVesselSelect")
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
            
        elapsed = time.time() - seg3_start
        if elapsed < durations[2]:
            page.wait_for_timeout(int((durations[2] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 4: Live Demo — Module 2 Satellite AIS Telematics & GIS (~55s)
        # -------------------------------------------------------------
        print(f"[Segment 4] Recording Satellite AIS Fleet Telematics (target: {durations[3]:.1f}s)...")
        seg4_start = time.time()
        
        # Navigate to Live Telematics panel
        page.click("[data-panel='telematics']")
        page.wait_for_timeout(3000)
        
        # Filter buttons: Capesize
        cape_btn = page.locator("#telematics-class-filters button[data-class='Capesize']")
        if cape_btn.count() > 0:
            cape_btn.click()
            page.wait_for_timeout(3500)
            
        # Filter buttons: Panamax
        panamax_btn = page.locator("#telematics-class-filters button[data-class='Panamax']")
        if panamax_btn.count() > 0:
            panamax_btn.click()
            page.wait_for_timeout(3500)
            
        # Filter buttons: All Fleet
        all_btn = page.locator("#telematics-class-filters button[data-class='ALL']")
        if all_btn.count() > 0:
            all_btn.click()
            page.wait_for_timeout(3500)
            
        # Hover over vessel cards in the right telematics feed
        vessel_cards = page.locator("#telematics-feed > div")
        card_count = vessel_cards.count()
        if card_count > 0:
            for i in range(min(card_count, 3)):
                vessel_cards.nth(i).hover()
                vessel_cards.nth(i).click()
                page.wait_for_timeout(4000)
                
        # Move mouse across map container
        map_elem = page.locator("#map-container")
        if map_elem.count() > 0:
            mbox = map_elem.bounding_box()
            if mbox:
                page.mouse.move(mbox["x"] + mbox["width"] * 0.5, mbox["y"] + mbox["height"] * 0.5)
                page.mouse.wheel(0, -300)  # zoom in
                page.wait_for_timeout(3000)
                page.mouse.wheel(0, 300)   # zoom out
                page.wait_for_timeout(3000)
                
        elapsed = time.time() - seg4_start
        if elapsed < durations[3]:
            page.wait_for_timeout(int((durations[3] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 5: Live Demo — Module 3 & 4 Draught Solver & Hedging Advisor (~52s)
        # -------------------------------------------------------------
        print(f"[Segment 5] Recording Vessel Optimizer & Contract Hedging (target: {durations[4]:.1f}s)...")
        seg5_start = time.time()
        
        # Click Vessel Optimizer
        page.click("#nav-vessel")
        page.wait_for_timeout(2500)
        
        # Change cargo volume
        cargo_input = page.locator("#vesselCargoInput")
        if cargo_input.count() > 0:
            cargo_input.fill("120000")
            page.wait_for_timeout(1500)
            page.click("#optimizeVesselBtn")
            page.wait_for_timeout(5000)
            
        # Click Port Infrastructure
        page.click("#nav-port")
        page.wait_for_timeout(2500)
        page.evaluate("window.scrollBy({top: 300, behavior: 'smooth'})")
        page.wait_for_timeout(3000)
        page.evaluate("window.scrollBy({top: -300, behavior: 'smooth'})")
        page.wait_for_timeout(2000)
        
        # Click Contract Strategy
        page.click("[data-panel='contract']")
        page.wait_for_timeout(2500)
        
        # Click Analyze Contract button
        analyze_btn = page.locator("#analyzeContractBtn")
        if analyze_btn.count() > 0:
            analyze_btn.click()
            page.wait_for_timeout(5000)
            
        # Scroll through contract recommendations
        page.evaluate("window.scrollBy({top: 400, behavior: 'smooth'})")
        page.wait_for_timeout(4000)
        page.evaluate("window.scrollBy({top: -400, behavior: 'smooth'})")
        page.wait_for_timeout(3000)
        
        elapsed = time.time() - seg5_start
        if elapsed < durations[4]:
            page.wait_for_timeout(int((durations[4] - elapsed) * 1000) + 500)
            
        # -------------------------------------------------------------
        # SEGMENT 6: Feasibility, Quantifiable ROI & Closing (~45s)
        # -------------------------------------------------------------
        print(f"[Segment 6] Recording Risk Console & Impact Summary (target: {durations[5]:.1f}s)...")
        seg6_start = time.time()
        
        # Navigate to Risk Alerts
        page.click("[data-panel='risk']")
        page.wait_for_timeout(3500)
        
        # Hover active alerts
        alerts_list = page.locator("#riskAlertsList")
        if alerts_list.count() > 0:
            alerts_list.hover()
            page.wait_for_timeout(3500)
            
        # Hover Volatility index chart
        vol_chart = page.locator("#volatilityChart")
        if vol_chart.count() > 0:
            vol_chart.hover()
            page.wait_for_timeout(3500)
            
        # Switch to AI Assistant panel
        page.click("[data-panel='ai']")
        page.wait_for_timeout(2500)
        
        # Click first suggested prompt
        first_prompt = page.locator("#ai-suggested-prompts span").first
        if first_prompt.count() > 0:
            first_prompt.click()
            page.wait_for_timeout(5000)
            
        # Return to main Rate Forecast for closing executive visual
        page.click("#nav-forecast")
        page.wait_for_timeout(2000)
        page.mouse.move(1280, 200)
        page.wait_for_timeout(4000)
        
        elapsed = time.time() - seg6_start
        if elapsed < durations[5]:
            page.wait_for_timeout(int((durations[5] - elapsed) * 1000) + 1000)
            
        # Finalize video recording
        video_path = page.video.path()
        context.close()
        browser.close()
        time.sleep(2)
        
    print(f"Playwright finished recording raw WebM video to: {video_path}")
    return video_path

def mux_final_mp4(webm_video, master_audio):
    """Mux 1440p video with natural master audio track using FFmpeg."""
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
        "-crf", "18",               # Near-lossless visual quality
        "-pix_fmt", "yuv420p",       # Standard 8-bit compatibility
        "-c:a", "aac",
        "-b:a", "192k",              # High fidelity audio
        "-shortest",
        FINAL_MP4
    ]
    
    print("Running command:", " ".join(cmd[:10]), "...")
    subprocess.run(cmd, check=True)
    
    size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    duration = get_media_duration(FINAL_MP4)
    print(f"\n[SUCCESS] Final 1440p Video Generated: {FINAL_MP4}")
    print(f"Resolution: 2560x1440 (1440p Quad HD)")
    print(f"Duration:   {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"File Size:  {size_mb:.2f} MB")
    print(f"Audio Voice: Microsoft Christopher Neural (Natural Human Male Presenter)")
    print("=" * 60)

def main():
    master_audio, durations = asyncio.run(generate_all_audio())
    webm_video = record_synchronized_walkthrough(durations)
    mux_final_mp4(webm_video, master_audio)

if __name__ == "__main__":
    main()
