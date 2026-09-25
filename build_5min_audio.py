import asyncio
import os
import edge_tts
import imageio_ffmpeg
import subprocess

VOICE = "en-US-ChristopherNeural"

SEGMENTS = [
    # --- PART 1: MAIN PART OF PROJECT (FIRST 3 MINUTES = 180 SECONDS) ---
    {
        "id": "seg1_intro",
        "title": "Project Identity & Strategic Mission",
        "target_dur": 36.0,
        "text": (
            "Welcome to the comprehensive presentation of SPECTRA, a next-generation "
            "High-Speed Radio Frequency Signal Intelligence and Automated Blind Demodulation "
            "platform engineered for the National Technical Research Organisation. In contemporary "
            "defense operations, military commanders confront a heavily congested and hostile "
            "electromagnetic spectrum, where frequency-agile radars, drone downlinks, and encrypted "
            "tactical radios constantly attempt to evade detection. SPECTRA bridges this gap with "
            "an autonomous, software-defined architecture delivering end-to-end signal analysis."
        )
    },
    {
        "id": "seg2_problem",
        "title": "Problem Statement & EW Challenges",
        "target_dur": 36.0,
        "text": (
            "The operational problem is severe. Traditional hardware receivers rely on rigid, pre-configured "
            "demodulators that fail when encountering non-cooperative signals, dynamic carrier frequency "
            "hops, or severe multi-path fading. Electronic warfare environments require real-time blind "
            "detection where carrier frequency, symbol rate, modulation scheme, and forward error correction "
            "parameters are completely unknown prior to interception. SPECTRA eliminates hardware lock-in, "
            "empowering SIGINT operators to intercept, classify, and decode unknown threats within milliseconds."
        )
    },
    {
        "id": "seg3_architecture",
        "title": "Technical Architecture & Ingestion Pipeline",
        "target_dur": 36.0,
        "text": (
            "At the architectural core lies SPECTRA's high-throughput three-tier processing pipeline. "
            "The physical ingestion layer streams raw In-Phase and Quadrature data at multi-gigabit rates, "
            "utilizing zero-copy memory buffers and SIMD-accelerated Fast Fourier Transforms. "
            "The streaming spectral engine executes real-time Short-Time Fourier Transforms and Doppler "
            "shift tracking, generating high-resolution waterfall heatmaps that isolate spectral emissions "
            "across expansive bandwidths without packet loss."
        )
    },
    {
        "id": "seg4_neural_amc",
        "title": "Deep Neural Modulation Classification",
        "target_dur": 36.0,
        "text": (
            "The second tier represents our Automatic Modulation Classification engine. Unlike traditional "
            "decision-tree algorithms that collapse under noise, SPECTRA employs a hybrid deep neural network "
            "combining convolutional feature extractors with temporal transformer attention. "
            "This neural engine evaluates cyclic spectral statistics and complex IQ constellation manifolds, "
            "achieving over ninety-five percent classification accuracy on complex modulations like QPSK, "
            "sixteen-QAM, and frequency-shift keying, even in hostile environments down to negative ten dB SNR."
        )
    },
    {
        "id": "seg5_protocol_fec",
        "title": "Protocol Layer & Mathematical Foundations",
        "target_dur": 36.0,
        "text": (
            "The third tier tackles symbol synchronization and protocol-level deinterleaving. "
            "Our DSP pipeline applies Gardner timing recovery and Costas loop carrier phase locking. "
            "Recovered symbol streams pass directly to hardware-accelerated Viterbi, Reed-Solomon, "
            "and Low-Density Parity-Check decoders for bitstream deframing. "
            "Our methodology is strictly grounded in peer-reviewed electronic warfare research from 2024 to 2026, "
            "surpassing conventional spectrum analyzers in speed, precision, and autonomous intelligence."
        )
    },
    # --- PART 2: THE REST OF THE PROJECT (REMAINING 2 MINUTES = 120 SECONDS) ---
    {
        "id": "seg6_live_waterfall",
        "title": "Live Interactive Mission Console & Waterfall",
        "target_dur": 40.0,
        "text": (
            "Now transitioning to the live operational application, operators interact with SPECTRA's "
            "tactical command console. Powered by hardware-accelerated WebGL rendering, the interface "
            "displays a sixty-frame-per-second real-time waterfall spectrograph. "
            "Operators can dynamically adjust FFT resolution, apply digital bandpass filters, zoom into "
            "transient RF bursts, and observe automated spectral emission masks. Continuous telemetry displays "
            "signal-to-noise ratio, instantaneous bandwidth, and carrier offset with sub-megahertz precision."
        )
    },
    {
        "id": "seg7_live_constellation",
        "title": "Live Demodulation & Bitstream Analytics",
        "target_dur": 40.0,
        "text": (
            "Moving directly into the demodulation laboratory, SPECTRA maps IQ data onto an interactive "
            "constellation diagram and eye pattern analyzer. When an unknown transmission is intercepted, "
            "the neural classifier outputs its confidence score in real time. The platform locks carrier phase, "
            "resolves constellation rotation, and renders the synchronized bitstream into raw hex dumps. "
            "Integrated entropy meters and frame synchronizers automatically detect packet headers, "
            "exposing payload contents for immediate intelligence assessment."
        )
    },
    {
        "id": "seg8_benchmarks_impact",
        "title": "Benchmarks, Defense Deployment & Roadmap",
        "target_dur": 40.0,
        "text": (
            "In rigorous benchmark evaluations, SPECTRA demonstrates end-to-end processing latency under "
            "ten milliseconds on commercial off-the-shelf edge hardware. This extreme efficiency enables "
            "seamless deployment across tactical UAV reconnaissance payloads, border surveillance towers, "
            "and naval electronic support measures. Designed for Smart India Hackathon 2026, SPECTRA delivers "
            "indigenous, sovereign defense technological capabilities, advancing national security through "
            "world-class RF intelligence innovation."
        )
    }
]

async def generate_segment_audio():
    os.makedirs("audio_output", exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    
    total_audio_dur = 0.0
    for idx, seg in enumerate(SEGMENTS):
        out_mp3 = os.path.join("audio_output", f"{seg['id']}.mp3")
        print(f"Generating audio for segment {idx+1}: {seg['title']}...")
        comm = edge_tts.Communicate(seg["text"], VOICE)
        await comm.save(out_mp3)
        
        # Check duration with ffmpeg
        res = subprocess.run([ffmpeg, "-i", out_mp3], capture_output=True, text=True)
        dur = 0.0
        for line in res.stderr.splitlines():
            if "Duration:" in line:
                parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
                dur = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
                break
        seg["measured_dur"] = dur
        total_audio_dur += dur
        print(f"  -> Generated: {dur:.2f}s (Target: {seg['target_dur']:.2f}s)")

    print(f"\nTotal raw spoken audio duration: {total_audio_dur:.2f}s ({total_audio_dur/60:.2f} mins)")
    return SEGMENTS

if __name__ == "__main__":
    asyncio.run(generate_segment_audio())
