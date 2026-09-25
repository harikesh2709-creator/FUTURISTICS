import asyncio
import os
import sys
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import imageio_ffmpeg

VOICE = "en-US-ChristopherNeural"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

TEMP_DIR = r"c:\vs studio\ntro-signal-analyzer\build_5min_temp"
OUTPUT_MP4 = r"c:\vs studio\ntro-signal-analyzer\SPECTRA_5Min_Project_Presentation.mp4"
WORKSPACE_COPY = r"c:\vs studio\SPECTRA_5Min_Project_Presentation.mp4"
ARTIFACT_DIR = r"C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb"

SEGMENTS = [
    # =========================================================================
    # PART 1: MAIN PART OF PROJECT (0:00 TO 3:00 = EXACTLY 180 SECONDS)
    # =========================================================================
    {
        "id": "seg1",
        "title": "SECTION 01/08: PROJECT IDENTITY & STRATEGIC MISSION",
        "timeline": "00:00 - 00:36 | PART 1: CORE ARCHITECTURE [1/5]",
        "subtitle": "NTRO RF SIGNAL INTELLIGENCE & DEMODULATION PLATFORM | SIH 2026 OFFICIAL RUBRIC",
        "type": "slide",
        "src": r"c:\vs studio\ntro-signal-analyzer\exported_strict_template_slides\slide_1.png",
        "target_dur": 36.0,
        "text": (
            "Welcome to the comprehensive technical briefing of Project SPECTRA, an advanced, "
            "military-grade Radio Frequency Signal Intelligence and Automated Blind Demodulation "
            "Platform engineered for the National Technical Research Organisation. In modern electronic "
            "warfare, military commanders face an increasingly dense and hostile electromagnetic spectrum, "
            "where agile frequency-hopping signals, covert drone telemetry, and low-probability-of-intercept "
            "transmissions evade conventional hardware receivers. SPECTRA solves this mission-critical "
            "challenge through a unified, high-throughput software-defined architecture delivering sovereign, "
            "real-time spectral intelligence."
        )
    },
    {
        "id": "seg2",
        "title": "SECTION 02/08: PROBLEM STATEMENT & ELECTRONIC WARFARE BOTTLENECKS",
        "timeline": "00:36 - 01:12 | PART 1: CORE ARCHITECTURE [2/5]",
        "subtitle": "CONGESTED RF SPECTRUM | AGILE FREQUENCY HOPPING | BLIND INTERCEPTION CHALLENGES",
        "type": "slide",
        "src": r"c:\vs studio\ntro-signal-analyzer\exported_strict_template_slides\slide_2.png",
        "target_dur": 36.0,
        "text": (
            "The operational challenge is severe. Traditional hardware spectrum analyzers rely on rigid, "
            "pre-configured superheterodyne demodulators that instantly fail when encountering non-cooperative "
            "signals, dynamic carrier frequency hops, or severe multi-path fading. Modern electronic warfare "
            "environments demand immediate blind interception where carrier frequencies, symbol rates, "
            "pulse shapes, and forward error correction protocols are completely unknown prior to capture. "
            "SPECTRA eliminates hardware lock-in, empowering defense operators to intercept, classify, "
            "and extract vital intelligence from unknown hostile threats in under ten milliseconds."
        )
    },
    {
        "id": "seg3",
        "title": "SECTION 03/08: 3-TIER PROCESSING PIPELINE & INGESTION ARCHITECTURE",
        "timeline": "01:12 - 01:48 | PART 1: CORE ARCHITECTURE [3/5]",
        "subtitle": "MULTI-GIGABIT I/Q STREAMING | ZERO-COPY RING BUFFER | SIMD-ACCELERATED STFT / FFT",
        "type": "slide",
        "src": r"c:\vs studio\ntro-signal-analyzer\exported_strict_template_slides\slide_3.png",
        "target_dur": 36.0,
        "text": (
            "At the architectural heart of SPECTRA lies our high-throughput three-tier processing pipeline. "
            "The physical ingestion layer captures raw In-Phase and Quadrature data streams at multi-gigabit "
            "rates, utilizing circular ring buffers with zero-copy memory pipelines and SIMD-accelerated "
            "Fast Fourier Transforms. The streaming spectral engine computes continuous Short-Time Fourier "
            "Transforms and Doppler shift tracking in real time, generating high-resolution waterfall heatmaps "
            "that isolate narrow-band emissions across expansive operational bandwidths without dropped samples."
        )
    },
    {
        "id": "seg4",
        "title": "SECTION 04/08: DEEP NEURAL AUTOMATIC MODULATION CLASSIFICATION (AMC)",
        "timeline": "01:48 - 02:24 | PART 1: CORE ARCHITECTURE [4/5]",
        "subtitle": "HYBRID CNN-TRANSFORMER ATTENTION | RESILIENT DOWN TO -10 dB SNR | >95% AMC ACCURACY",
        "type": "slide",
        "src": r"c:\vs studio\ntro-signal-analyzer\exported_strict_template_slides\slide_4.png",
        "target_dur": 36.0,
        "text": (
            "The second tier represents our Automatic Modulation Classification neural laboratory. Unlike "
            "legacy decision-tree algorithms that collapse under adverse channel noise, SPECTRA deploys a "
            "hybrid deep neural network combining convolutional spatial feature extractors with temporal "
            "transformer attention mechanisms. This neural engine analyzes cyclic spectral statistics and complex "
            "IQ constellation manifolds, achieving over ninety-five percent classification accuracy across digital "
            "modulations including QPSK, sixteen-QAM, and frequency-shift keying, maintaining high resilience "
            "even in hostile environments down to negative ten dB SNR."
        )
    },
    {
        "id": "seg5",
        "title": "SECTION 05/08: PROTOCOL FEC LAYER & 2024-2026 RESEARCH CITATIONS",
        "timeline": "02:24 - 03:00 | PART 1: CORE ARCHITECTURE [5/5]",
        "subtitle": "GARDNER TIMING & COSTAS LOOP | VITERBI / LDPC DECODERS | IEEE PEER-REVIEWED METHODOLOGY",
        "type": "slide",
        "src": r"c:\vs studio\ntro-signal-analyzer\exported_strict_template_slides\slide_5.png",
        "target_dur": 36.0,
        "text": (
            "The third tier executes symbol synchronization and protocol-level deinterleaving. Our DSP pipeline "
            "applies Gardner timing recovery and Costas loop carrier phase locking to extract discrete symbol "
            "sequences. These recovered streams pass directly into hardware-accelerated Viterbi, Reed-Solomon, "
            "and Low-Density Parity-Check decoders for bitstream deframing. Our technical approach is strictly "
            "validated against peer-reviewed electronic warfare research from 2024 to 2026, demonstrating "
            "mathematically proven superiority over conventional spectrum analyzers in detection probability "
            "and computational efficiency."
        )
    },

    # =========================================================================
    # PART 2: THE REST OF THE PROJECT (3:00 TO 5:00 = EXACTLY 120 SECONDS)
    # =========================================================================
    {
        "id": "seg6",
        "title": "SECTION 06/08: LIVE DEMO // TACTICAL CONSOLE & REAL-TIME WATERFALL",
        "timeline": "03:00 - 03:40 | PART 2: LIVE DEMO & IMPACT [1/3]",
        "subtitle": "● LIVE INTERACTIVE APPLICATION | 60 FPS WEBGL WATERFALL | DYNAMIC FFT RESOLUTION & FILTERS",
        "type": "animated_webp",
        "src": os.path.join(ARTIFACT_DIR, "spectra_clean_nav_1789464784712.webp"),
        "target_dur": 40.0,
        "text": (
            "Now transitioning directly into the live operational application, operators interact with "
            "SPECTRA's tactical command console. Powered by hardware-accelerated WebGL rendering, the "
            "interface displays a sixty-frame-per-second real-time waterfall spectrograph. Operators can "
            "dynamically adjust FFT windowing, apply digital bandpass filters, zoom into microsecond-duration "
            "RF bursts, and observe automated spectral emission masks. Live telemetry feeds continuously report "
            "signal-to-noise ratio, instantaneous bandwidth, and Doppler carrier offsets with sub-megahertz precision, "
            "ensuring comprehensive situational awareness across active frequency bands."
        )
    },
    {
        "id": "seg7",
        "title": "SECTION 07/08: LIVE DEMO // NEURAL DEMODULATION & BITSTREAM RECOVERY",
        "timeline": "03:40 - 04:20 | PART 2: LIVE DEMO & IMPACT [2/3]",
        "subtitle": "● LIVE INTERACTIVE APPLICATION | CONSTELLATION SCATTER & EYE DIAGRAM | HEX BITSTREAM DEFRAMER",
        "type": "animated_webp",
        "src": os.path.join(ARTIFACT_DIR, "verify_new_dashboard_1789139193706.webp"),
        "target_dur": 40.0,
        "text": (
            "Moving into the live demodulation suite, SPECTRA maps raw IQ data onto an interactive "
            "constellation scatter plot and eye diagram analyzer. When an unknown transmission is intercepted, "
            "the neural classifier calculates classification confidence in real time. The engine locks carrier phase, "
            "removes phase ambiguity, and decodes the stream into raw hexadecimal bitstreams. Integrated "
            "entropy analyzers and frame synchronizers automatically detect preamble headers, displaying decoded "
            "packet payloads and ASCII telemetry for instantaneous threat identification and military intelligence "
            "exploitation."
        )
    },
    {
        "id": "seg8",
        "title": "SECTION 08/08: PERFORMANCE BENCHMARKS, DEFENSE DEPLOYMENT & ROADMAP",
        "timeline": "04:20 - 05:00 | PART 2: LIVE DEMO & IMPACT [3/3]",
        "subtitle": "<10ms PROCESSING LATENCY | UAV & BORDER RADAR DEPLOYMENT | ATMANIRBHAR BHARAT SIH 2026",
        "type": "slide",
        "src": r"c:\vs studio\ntro-signal-analyzer\exported_strict_template_slides\slide_6.png",
        "target_dur": 40.0,
        "text": (
            "In comprehensive benchmark evaluations, SPECTRA demonstrates end-to-end processing latency under "
            "ten milliseconds on commercial off-the-shelf edge computing hardware. This extreme efficiency "
            "unlocks direct integration into tactical drone reconnaissance pods, border surveillance radar "
            "towers, and naval electronic support systems. Developed for Smart India Hackathon 2026, SPECTRA "
            "delivers an indigenous, sovereign defense capability for the National Technical Research Organisation, "
            "ensuring national electromagnetic spectrum superiority through world-class Indian engineering."
        )
    }
]

def get_audio_duration(file_path):
    res = subprocess.run([FFMPEG, "-i", file_path], capture_output=True, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    return 0.0

async def build_audio_tracks():
    print("\n--- STEP 1: GENERATING VOICE OVER AUDIO WITH MICROPHONE-GRADE NEURAL TTS ---")
    audio_segments = []
    
    for idx, seg in enumerate(SEGMENTS):
        raw_mp3 = os.path.join(TEMP_DIR, f"{seg['id']}_raw.mp3")
        padded_wav = os.path.join(TEMP_DIR, f"{seg['id']}_padded.wav")
        target_dur = seg["target_dur"]
        
        print(f"\n[Segment {idx+1}/8] Generating voiceover for: {seg['title']}")
        comm = edge_tts.Communicate(seg["text"], VOICE)
        await comm.save(raw_mp3)
        
        raw_dur = get_audio_duration(raw_mp3)
        print(f"  Raw voice duration: {raw_dur:.2f}s (Target duration: {target_dur:.2f}s)")
        
        # Pad with silence or adjust to reach exact target duration
        if raw_dur < target_dur:
            pad_needed = target_dur - raw_dur
            # Use apad filter in ffmpeg to pad to exact target duration
            cmd = [
                FFMPEG, "-y",
                "-i", raw_mp3,
                "-af", f"apad=pad_dur={pad_needed:.3f}",
                "-t", f"{target_dur:.3f}",
                "-c:a", "pcm_s16le",
                "-ar", "48000",
                padded_wav
            ]
        else:
            # If slightly over, scale tempo slightly to fit exactly
            ratio = raw_dur / target_dur
            cmd = [
                FFMPEG, "-y",
                "-i", raw_mp3,
                "-af", f"atempo={ratio:.4f}",
                "-t", f"{target_dur:.3f}",
                "-c:a", "pcm_s16le",
                "-ar", "48000",
                padded_wav
            ]
        
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        final_dur = get_audio_duration(padded_wav)
        print(f"  Padded audio duration: {final_dur:.2f}s (Target: {target_dur:.2f}s)")
        audio_segments.append(padded_wav)

    # Concatenate all 8 audio tracks
    concat_list_path = os.path.join(TEMP_DIR, "audio_concat.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in audio_segments:
            safe_p = p.replace("\\", "/")
            f.write(f"file '{safe_p}'\n")

    master_audio_path = os.path.join(TEMP_DIR, "master_audio_5min.wav")
    cmd_cat = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c:a", "pcm_s16le",
        master_audio_path
    ]
    subprocess.run(cmd_cat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    master_dur = get_audio_duration(master_audio_path)
    print(f"\n Master Audio Built! Total Duration: {master_dur:.2f}s ({master_dur/60:.2f} minutes)")
    return master_audio_path

def apply_hud_overlay(img, title, timeline, subtitle):
    target_w, target_h = 1920, 1080
    
    # Scale or center onto 1920x1080 canvas
    if img.size != (target_w, target_h):
        w, h = img.size
        # Maintain aspect ratio
        ratio = min(target_w / w, (target_h - 100) / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        bg = Image.new("RGB", (target_w, target_h), (9, 13, 22))
        pad_x = (target_w - new_w) // 2
        pad_y = 50 + (target_h - 100 - new_h) // 2
        bg.paste(img_resized, (pad_x, pad_y))
        canvas = bg
    else:
        canvas = img.copy()

    draw = ImageDraw.Draw(canvas)
    try:
        font_main = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 23)
        font_mono = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 19)
        font_badge = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)
    except:
        font_main = ImageFont.load_default()
        font_mono = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Top HUD Bar (Translucent glass dark bar with glowing cyan border)
    draw.rectangle([(0, 0), (1920, 48)], fill=(8, 14, 26))
    draw.line([(0, 48), (1920, 48)], fill=(0, 210, 255), width=2)
    
    # Draw glowing status dot
    draw.ellipse([(28, 18), (38, 28)], fill=(0, 255, 180), outline=(0, 210, 255))
    draw.text((48, 12), "[SPECTRA // NTRO DEFENSE SIGINT]", fill=(0, 225, 255), font=font_mono)
    draw.text((540, 12), title, fill=(255, 255, 255), font=font_main)
    draw.text((1500, 12), timeline, fill=(0, 225, 255), font=font_mono)

    # Bottom Telemetry Bar
    draw.rectangle([(0, 1032), (1920, 1080)], fill=(8, 14, 26))
    draw.line([(0, 1032), (1920, 1032)], fill=(0, 210, 255), width=2)
    draw.text((30, 1045), subtitle, fill=(185, 230, 255), font=font_mono)
    draw.text((1650, 1045), "DEFENSE CLASSIFIED // LIVE", fill=(0, 255, 180), font=font_badge)

    return canvas

def build_video_tracks():
    print("\n--- STEP 2: GENERATING BROADCAST 1080p 30fps VIDEO TRACKS ---")
    video_segments = []

    for idx, seg in enumerate(SEGMENTS):
        print(f"\n[Segment {idx+1}/8] Rendering video for: {seg['title']}")
        target_dur = seg["target_dur"]
        seg_mp4 = os.path.join(TEMP_DIR, f"{seg['id']}_video.mp4")

        if seg["type"] == "slide":
            # Process static slide with HUD
            slide_img = Image.open(seg["src"]).convert("RGB")
            hud_img = apply_hud_overlay(slide_img, seg["title"], seg["timeline"], seg["subtitle"])
            hud_png = os.path.join(TEMP_DIR, f"{seg['id']}_hud.png")
            hud_img.save(hud_png)

            # Generate video with ffmpeg loop
            cmd = [
                FFMPEG, "-y",
                "-loop", "1",
                "-t", f"{target_dur:.3f}",
                "-i", hud_png,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                "-preset", "ultrafast",
                seg_mp4
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"  Slide video generated ({target_dur:.1f}s)")

        elif seg["type"] == "animated_webp":
            # Process animated webp recording
            im = Image.open(seg["src"])
            n_webp_frames = getattr(im, "n_frames", 1)
            print(f"  Extracting & overlaying HUD on {n_webp_frames} webp frames...")
            
            cached_frames = []
            for fi in range(n_webp_frames):
                im.seek(fi)
                f_rgb = im.convert("RGB")
                hud_f = apply_hud_overlay(f_rgb, seg["title"], seg["timeline"], seg["subtitle"])
                cached_frames.append(hud_f.tobytes())

            total_video_frames = int(target_dur * 30) # 30 fps
            print(f"  Piping {total_video_frames} frames ({target_dur:.1f}s @ 30fps) into H.264 encoder...")

            cmd = [
                FFMPEG, "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", "1920x1080",
                "-pix_fmt", "rgb24",
                "-r", "30",
                "-i", "-",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "ultrafast",
                "-t", f"{target_dur:.3f}",
                seg_mp4
            ]
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for vfi in range(total_video_frames):
                w_idx = int(vfi * n_webp_frames / total_video_frames) % n_webp_frames
                proc.stdin.write(cached_frames[w_idx])
            proc.stdin.close()
            proc.wait()
            print(f"  Live animated demo video generated ({target_dur:.1f}s)")

        video_segments.append(seg_mp4)

    # Concatenate all 8 video tracks
    concat_list_path = os.path.join(TEMP_DIR, "video_concat.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in video_segments:
            safe_p = p.replace("\\", "/")
            f.write(f"file '{safe_p}'\n")

    master_video_path = os.path.join(TEMP_DIR, "master_video_5min.mp4")
    cmd_cat = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c:v", "copy",
        master_video_path
    ]
    subprocess.run(cmd_cat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    v_dur = get_audio_duration(master_video_path)
    print(f"\n Master Video Built! Total Duration: {v_dur:.2f}s ({v_dur/60:.2f} minutes)")
    return master_video_path

def finalize_master_production(master_video_path, master_audio_path):
    print("\n--- STEP 3: FINAL MULTIPLEXING & MASTER RENDER (1080p 60fps/30fps FULL AUDIO-VISUAL MP4) ---")
    
    cmd_mux = [
        FFMPEG, "-y",
        "-i", master_video_path,
        "-i", master_audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        OUTPUT_MP4
    ]
    subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    final_dur = get_audio_duration(OUTPUT_MP4)
    file_size_mb = os.path.getsize(OUTPUT_MP4) / (1024 * 1024)
    print(f"\n=======================================================================")
    print(f" SPECTRA 5-MINUTE MASTER PRESENTATION VIDEO CREATED!")
    print(f" Location: {OUTPUT_MP4}")
    print(f" Duration: {final_dur:.2f}s ({final_dur/60:.2f} minutes / 5:00)")
    print(f" File Size: {file_size_mb:.2f} MB")
    print(f" Resolution: 1920x1080 (Full HD, 30 FPS, H.264 / AAC 256k)")
    print(f" Voice: Microsoft Christopher Neural (Rich, Clear, Authoritative Male)")
    print(f"=======================================================================\n")

    # Copy to workspace root and artifact directory for convenience
    try:
        import shutil
        shutil.copy2(OUTPUT_MP4, WORKSPACE_COPY)
        print(f" Copied to Workspace Root: {WORKSPACE_COPY}")
        artifact_dest = os.path.join(ARTIFACT_DIR, "SPECTRA_5Min_Project_Presentation.mp4")
        shutil.copy2(OUTPUT_MP4, artifact_dest)
        print(f" Copied to Artifacts Directory: {artifact_dest}")
    except Exception as e:
        print(f"Note on copy: {e}")

async def main():
    t_start = time.time()
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    master_audio = await build_audio_tracks()
    master_video = build_video_tracks()
    finalize_master_production(master_video, master_audio)
    
    print(f" Total pipeline execution time: {time.time()-t_start:.1f}s")

if __name__ == "__main__":
    asyncio.run(main())
