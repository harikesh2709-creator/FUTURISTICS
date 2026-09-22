import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

def generate_architecture_diagram():
    assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
    os.makedirs(assets_dir, exist_ok=True)
    out_path = os.path.join(assets_dir, 'system_architecture_drawio.png')

    # Dimensions matching exact 2.76:1 aspect ratio for Slide 3 Box 2 (5.65" x 2.05")
    fig_w, fig_h = 13.8, 5.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)

    # Background matches SIH card background #F1F6FE exactly
    bg_color = '#F1F6FE'
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.axis('off')
    ax.set_xlim(0, 13.8)
    ax.set_ylim(0, 5.0)

    # Colors
    c_card_bg = '#FFFFFF'
    c_card_border = '#CBD5E1'
    c_navy = '#0F172A'
    c_text = '#1E293B'
    c_muted = '#475569'
    
    # Stage accent colors
    stages = [
        {
            "num": "STAGE 1",
            "title": "INGESTION & FRONT-END",
            "accent": "#2563EB",       # Blue
            "light_accent": "#EFF6FF",
            "badge_text": "#1E40AF",
            "x": 0.40, "w": 2.30,
            "blocks": [
                ("Raw .IQ (Float32 / Int16)", "Baseband capture files"),
                ("High-Rate .wav Audio", "Spacecraft telemetry"),
                ("Automated DC Nulling", "Hardware LO leakage removal"),
                ("Polyphase Channelizer", "Sub-band decimation filter"),
                ("Welch PSD & Waterfall", "Real-time spectral analysis")
            ]
        },
        {
            "num": "STAGE 2",
            "title": "FEATURE & NEURAL AMC",
            "accent": "#7C3AED",       # Purple
            "light_accent": "#F5F3FF",
            "badge_text": "#5B21B6",
            "x": 3.00, "w": 2.35,
            "blocks": [
                ("Cyclostationary CAF", "Sx^α(f) baud rate recovery"),
                ("Higher-Order Cumulants", "C40, C42, C63 statistics"),
                ("1D-CNN + Bi-LSTM AMC", "10-class modulation in <35ms"),
                ("SNR & Doppler Estimator", "Adaptive thresholding (-4 dB)"),
                ("Blind Constellation Map", "Symmetry & order detection")
            ]
        },
        {
            "num": "STAGE 3",
            "title": "SYNC & DEMODULATION",
            "accent": "#D97706",       # Amber
            "light_accent": "#FFFBEB",
            "badge_text": "#92400E",
            "x": 5.65, "w": 2.35,
            "blocks": [
                ("Gardner Timing TED", "Symbol timing synchronization"),
                ("4th-Power Carrier FFT", "Coarse frequency offset lock"),
                ("Costas Phase Loop (PLL)", "Fine carrier phase tracking"),
                ("Optimal Matched Filter", "Root-Raised Cosine (RRC)"),
                ("Soft Symbol Demapper", "Log-Likelihood Ratio (LLR)")
            ]
        },
        {
            "num": "STAGE 4",
            "title": "SOLVER & FEC DECODE",
            "accent": "#059669",       # Emerald
            "light_accent": "#ECFDF5",
            "badge_text": "#065F46",
            "x": 8.30, "w": 2.35,
            "blocks": [
                ("Galois Field GF(2) Solver", "Blind interleaver depth D"),
                ("Matrix Rank Algorithm", "Linear algebraic rank parity"),
                ("Viterbi Trellis Decoder", "CCSDS Convolutional r=1/2"),
                ("Reed-Solomon (255,223)", "Syndrome error correction"),
                ("Frame Synchronizer", "ASM & sync-word detection")
            ]
        },
        {
            "num": "STAGE 5",
            "title": "SOVEREIGN C4ISR",
            "accent": "#0F172A",       # Dark Slate / Navy
            "light_accent": "#F8FAFC",
            "badge_text": "#0F172A",
            "x": 10.95, "w": 2.20,
            "blocks": [
                ("Decoded Bitstream Hex", "Extracted plaintext telemetry"),
                ("WebGL 60fps Telemetry", "Live constellation & eye diag"),
                ("Radar Threat Scoring", "Autonomous emitter risk eval"),
                ("SHA-256 Audit Dossier", "Cryptographic chain-of-custody"),
                ("100% Air-Gapped Engine", "Zero cloud dependency / leakage")
            ]
        }
    ]

    card_y = 0.25
    card_h = 3.90

    # Top title bar in diagram with proper spacing
    ax.text(6.90, 4.68, "SPECTRA END-TO-END AUTONOMOUS SIGNAL PROCESSING ARCHITECTURE & DATA FLOW",
            fontsize=11.5, fontweight='bold', color='#1E3A8A', ha='center', va='center', family='sans-serif')
    ax.text(6.90, 4.32, "Raw Baseband Intercept  ──►  Blind Parameter & Modulation Extraction  ──►  Synchronization  ──►  Blind FEC Solving  ──►  Actionable C4ISR",
            fontsize=8.0, fontweight='bold', color='#475569', ha='center', va='center', family='sans-serif')

    for stg in stages:
        x, w = stg["x"], stg["w"]
        
        # Outer Stage Box
        outer = patches.FancyBboxPatch(
            (x, card_y), w, card_h,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            facecolor=c_card_bg,
            edgecolor=stg["accent"],
            linewidth=1.6,
            zorder=2
        )
        ax.add_patch(outer)

        # Stage Header Background
        header_bg = patches.FancyBboxPatch(
            (x + 0.04, card_y + card_h - 0.65), w - 0.08, 0.60,
            boxstyle="round,pad=0.03,rounding_size=0.08",
            facecolor=stg["light_accent"],
            edgecolor='none',
            zorder=3
        )
        ax.add_patch(header_bg)

        # Stage Header Text
        ax.text(x + w/2, card_y + card_h - 0.22, stg["num"],
                fontsize=7.5, fontweight='bold', color=stg["badge_text"], ha='center', va='center', family='sans-serif', zorder=4)
        ax.text(x + w/2, card_y + card_h - 0.46, stg["title"],
                fontsize=8.0, fontweight='bold', color=stg["accent"], ha='center', va='center', family='sans-serif', zorder=4)

        # Blocks inside stage
        block_y_start = card_y + card_h - 0.80
        block_h = 0.52
        gap = 0.10

        for idx, (b_title, b_sub) in enumerate(stg["blocks"]):
            by = block_y_start - (idx + 1) * (block_h + gap) + gap
            
            # Sub-card
            sub_box = patches.FancyBboxPatch(
                (x + 0.10, by), w - 0.20, block_h,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                facecolor='#F8FAFC',
                edgecolor=c_card_border,
                linewidth=0.8,
                zorder=3
            )
            ax.add_patch(sub_box)

            # Left mini color pill indicator
            pill = patches.Rectangle(
                (x + 0.10, by), 0.05, block_h,
                facecolor=stg["accent"], edgecolor='none', zorder=4
            )
            ax.add_patch(pill)

            # Text inside sub-card
            ax.text(x + 0.20, by + block_h - 0.18, b_title,
                    fontsize=7.2, fontweight='bold', color=c_text, va='center', family='sans-serif', zorder=4)
            ax.text(x + 0.20, by + 0.15, b_sub,
                    fontsize=6.0, color=c_muted, va='center', family='sans-serif', zorder=4)

    # Connector arrows between stages
    arrow_labels = [
        ("Baseband\nIQ / wav", 2.85, 2.35),
        ("Modulation\n& Baud", 5.50, 2.35),
        ("Soft Bits\n& Symbols", 8.15, 2.35),
        ("Decoded\nFrames", 10.80, 2.35),
    ]

    for lbl, ax_pos, ay_pos in arrow_labels:
        # Arrow line
        ax.annotate("", xy=(ax_pos + 0.12, ay_pos), xytext=(ax_pos - 0.12, ay_pos),
                    arrowprops=dict(arrowstyle="-|>", color='#2563EB', lw=2.0, mutation_scale=12),
                    zorder=5)
        # Arrow label badge
        ax.text(ax_pos, ay_pos + 0.32, lbl,
                fontsize=5.8, fontweight='bold', color='#1E40AF', ha='center', va='center', family='sans-serif',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#EFF6FF', edgecolor='#93C5FD', lw=0.6),
                zorder=6)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Successfully generated clean Draw.io architecture diagram at: {out_path}")

if __name__ == "__main__":
    generate_architecture_diagram()
