import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_hd_architecture_diagram():
    assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
    os.makedirs(assets_dir, exist_ok=True)
    out_path_slide = os.path.join(assets_dir, 'system_architecture_hd.png')
    out_path_4k = os.path.join(assets_dir, 'spectra_high_definition_architecture_4k.png')

    # Dimensions matching exact 2.76:1 aspect ratio for Slide 3 Box 2 (13.8" x 5.0")
    fig_w, fig_h = 13.8, 5.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=350)

    # Background matches SIH card background #F1F6FE exactly
    bg_color = '#F1F6FE'
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.axis('off')
    ax.set_xlim(0, 13.8)
    ax.set_ylim(0, 5.0)

    c_text = '#0F172A'
    c_muted = '#334155'

    stages = [
        {
            "num": "01",
            "title": "RF SENSING",
            "sub": "Baseband IQ Stream",
            "color": "#2563EB", # Bold Blue
            "bg": "#DBEAFE",
            "x": 0.2, "w": 2.3,
            "desc": "• SDR dual-channel\n• 40 MSPS ingestion\n• Welch PSD Engine"
        },
        {
            "num": "02",
            "title": "DSP ENGINE",
            "sub": "Feature Extraction",
            "color": "#7C3AED", # Bold Purple
            "bg": "#EDE9FE",
            "x": 2.9, "w": 2.3,
            "desc": "• Cumulants (C40, C63)\n• Spectral correlation\n• SNR Enhancement"
        },
        {
            "num": "03",
            "title": "NEURAL AI",
            "sub": "Modulation & Sync",
            "color": "#EA580C", # Bold Orange
            "bg": "#FFEDD5",
            "x": 5.6, "w": 2.3,
            "desc": "• 1D-CNN + ResNet\n• Gardner TED timing\n• Costas PLL lock"
        },
        {
            "num": "04",
            "title": "FEC SOLVER",
            "sub": "Blind Decoding",
            "color": "#059669", # Bold Green
            "bg": "#D1FAE5",
            "x": 8.3, "w": 2.3,
            "desc": "• GF(2) matrix rank\n• Viterbi decoder\n• Frame assembly"
        },
        {
            "num": "05",
            "title": "C4ISR UI",
            "sub": "Tactical Display",
            "color": "#1E293B", # Dark Slate
            "bg": "#F1F5F9",
            "x": 11.0, "w": 2.3,
            "desc": "• 60fps WebGL canvas\n• Threat ranking\n• Air-gapped secure"
        }
    ]

    card_y = 0.5
    card_h = 3.6

    for i, stg in enumerate(stages):
        x, w = stg["x"], stg["w"]
        c = stg["color"]
        
        # Main shadow
        shadow = patches.FancyBboxPatch(
            (x + 0.08, card_y - 0.08), w, card_h,
            boxstyle="round,pad=0.0,rounding_size=0.15",
            facecolor="#CBD5E1", edgecolor='none', zorder=1, alpha=0.6
        )
        ax.add_patch(shadow)

        # Main box
        outer = patches.FancyBboxPatch(
            (x, card_y), w, card_h,
            boxstyle="round,pad=0.0,rounding_size=0.15",
            facecolor="white", edgecolor=c, linewidth=2.5, zorder=2
        )
        ax.add_patch(outer)

        # Header block
        header_h = 1.2
        header_y = card_y + card_h - header_h
        
        # Clip header to rounded corners via a smaller box (approximate)
        header_bg = patches.FancyBboxPatch(
            (x+0.02, header_y), w-0.04, header_h-0.02,
            boxstyle="round,pad=0.0,rounding_size=0.12",
            facecolor=c, edgecolor='none', zorder=3
        )
        ax.add_patch(header_bg)
        
        # Fix the bottom corners of header to be square
        header_sq = patches.Rectangle(
            (x+0.02, header_y), w-0.04, 0.2,
            facecolor=c, edgecolor='none', zorder=3
        )
        ax.add_patch(header_sq)

        # Text in header
        ax.text(x + 0.2, header_y + 0.85, stg["num"], fontsize=28, fontweight='black', color='white', alpha=0.3, zorder=4)
        ax.text(x + w/2, header_y + 0.55, stg["title"], fontsize=16, fontweight='bold', color='white', ha='center', zorder=4)
        ax.text(x + w/2, header_y + 0.20, stg["sub"], fontsize=11, color=stg["bg"], ha='center', zorder=4)

        # Description text
        ax.text(x + 0.25, card_y + 1.2, stg["desc"], fontsize=13, linespacing=1.8, color=c_text, fontweight='bold', va='center', zorder=4)

        # Draw connecting arrow if not last
        if i < len(stages) - 1:
            ax_pos = x + w + 0.1
            ay_pos = card_y + card_h / 2
            ax.annotate("", xy=(ax_pos + 0.35, ay_pos), xytext=(ax_pos - 0.05, ay_pos),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.8,head_length=1.0", color='#94A3B8', lw=4.5),
                        zorder=5)

    plt.tight_layout()
    plt.savefig(out_path_slide, dpi=350, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(out_path_4k, dpi=450, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated ultra-bold architecture diagram.")

if __name__ == "__main__":
    generate_hd_architecture_diagram()
