import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

assets_dir = r"c:\vs studio\ntro-signal-analyzer\presentation_assets"
os.makedirs(assets_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. Slide 2 Center Callout Diagram (Tactical Receiver & Callouts)
# -------------------------------------------------------------
def create_callout_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 7.5), dpi=300)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Draw Central Handheld/Tactical Device Body
    chassis = patches.FancyBboxPatch((3.0, 1.8), 4.0, 6.2, boxstyle="round,pad=0.3,rounding_size=0.4",
                                    facecolor='#1e293b', edgecolor='#334155', linewidth=3)
    ax.add_patch(chassis)

    # Antenna
    antenna = patches.Rectangle((3.6, 8.2), 0.45, 1.4, facecolor='#0f172a', edgecolor='#334155', linewidth=1.5)
    ax.add_patch(antenna)
    knob = patches.Circle((6.2, 8.3), 0.35, facecolor='#475569', edgecolor='#1e293b', linewidth=1.5)
    ax.add_patch(knob)

    # Screen bezel
    bezel = patches.Rectangle((3.4, 4.0), 3.2, 3.6, facecolor='#090d16', edgecolor='#475569', linewidth=2)
    ax.add_patch(bezel)

    # Screen display content (Spectrogram + Constellation preview)
    im_data = np.random.rand(30, 60)
    im_data[10:14, :] += 2.0  # signal carrier
    im_data[18:22, 20:45] += 2.5
    ax.imshow(im_data, extent=[3.5, 6.5, 5.7, 7.4], aspect='auto', cmap='turbo', origin='lower')
    ax.text(3.6, 7.15, "SPECTRA · NTRO SIGINT", color='#ffffff', fontsize=6.8, fontweight='bold', fontfamily='sans-serif')
    ax.text(5.5, 7.15, "LIVE IQ/WAV", color='#38bdf8', fontsize=6, fontweight='bold', fontfamily='sans-serif')

    # Lower half: Constellation & Metrics
    ax.text(3.55, 5.35, "AMC: 16-QAM (98.4%)", color='#4ade80', fontsize=7, fontweight='bold', fontfamily='sans-serif')
    ax.text(3.55, 5.0, "BAUD: 2.048 MBd", color='#facc15', fontsize=7, fontweight='bold', fontfamily='sans-serif')
    ax.text(3.55, 4.65, "SNR: 18.4 dB (-4dB Min)", color='#38bdf8', fontsize=6.8, fontweight='bold', fontfamily='sans-serif')
    ax.text(3.55, 4.3, "GF(2) D: 64 | BER: 1.2e-5", color='#a78bfa', fontsize=6.8, fontweight='bold', fontfamily='sans-serif')

    # Draw mini 16-QAM constellation dots on right of screen
    np.random.seed(42)
    cx = [5.6, 6.2, 5.6, 6.2]
    cy = [5.1, 5.1, 4.5, 4.5]
    for x0, y0 in zip(cx, cy):
        pts_x = x0 + np.random.normal(0, 0.05, 18)
        pts_y = y0 + np.random.normal(0, 0.05, 18)
        ax.scatter(pts_x, pts_y, color='#00f0ff', s=2.5, alpha=0.85)

    # Device Controls / Buttons
    for i in range(3):
        btn = patches.Circle((4.1 + i*0.9, 3.2), 0.22, facecolor='#334155', edgecolor='#64748b', linewidth=1)
        ax.add_patch(btn)
    # Speaker grill / d-pad
    dpad = patches.Circle((5.0, 2.3), 0.45, facecolor='#0f172a', edgecolor='#475569', linewidth=1.5)
    ax.add_patch(dpad)

    # 5 Callout Cards with Arrows tailored 100% to SPECTRA
    # Callout 1 (Top Left): Dual Ingestion
    box1 = patches.FancyBboxPatch((0.2, 7.2), 2.5, 1.2, boxstyle="round,pad=0.1,rounding_size=0.15",
                                 facecolor='#fef08a', edgecolor='#ca8a04', linewidth=1.2)
    ax.add_patch(box1)
    ax.text(1.45, 7.8, "Raw .IQ & .wav\nDual-Ingestion", ha='center', va='center', fontsize=8, fontweight='bold', color='#713f12')
    ax.annotate('', xy=(3.5, 7.6), xytext=(2.7, 7.7),
                arrowprops=dict(arrowstyle="->", color='#854d0e', lw=1.5))

    # Callout 2 (Middle Left): Cyclostationary & Cumulant AMC
    box2 = patches.FancyBboxPatch((0.1, 4.8), 2.7, 1.3, boxstyle="round,pad=0.1,rounding_size=0.15",
                                 facecolor='#ccfbf1', edgecolor='#0d9488', linewidth=1.2)
    ax.add_patch(box2)
    ax.text(1.45, 5.45, "Cyclostationary &\nCumulant AMC", ha='center', va='center', fontsize=8, fontweight='bold', color='#115e59')
    ax.annotate('', xy=(3.3, 5.2), xytext=(2.8, 5.4),
                arrowprops=dict(arrowstyle="->", color='#0f766e', lw=1.5))

    # Callout 3 (Bottom Left): GF(2) Blind Interleaver Solver
    box3 = patches.FancyBboxPatch((0.1, 2.0), 2.7, 1.3, boxstyle="round,pad=0.1,rounding_size=0.15",
                                 facecolor='#e0e7ff', edgecolor='#4f46e5', linewidth=1.2)
    ax.add_patch(box3)
    ax.text(1.45, 2.65, "GF(2) Blind\nInterleaver Solver", ha='center', va='center', fontsize=8, fontweight='bold', color='#312e81')
    ax.annotate('', xy=(3.1, 2.8), xytext=(2.8, 2.6),
                arrowprops=dict(arrowstyle="->", color='#4338ca', lw=1.5))

    # Callout 4 (Top Right): ESP32 USB HIL Testbench
    box4 = patches.FancyBboxPatch((7.2, 6.8), 2.6, 1.2, boxstyle="round,pad=0.1,rounding_size=0.15",
                                 facecolor='#e0f2fe', edgecolor='#0284c7', linewidth=1.2)
    ax.add_patch(box4)
    ax.text(8.5, 7.4, "ESP32 USB HIL\nTestbench Link", ha='center', va='center', fontsize=8, fontweight='bold', color='#0369a1')
    ax.annotate('', xy=(6.7, 6.6), xytext=(7.2, 7.3),
                arrowprops=dict(arrowstyle="->", color='#0284c7', lw=1.5))

    # Callout 5 (Bottom Right): Air-Gapped Sovereign Security
    box5 = patches.FancyBboxPatch((7.2, 3.4), 2.6, 1.2, boxstyle="round,pad=0.1,rounding_size=0.15",
                                 facecolor='#fecaca', edgecolor='#dc2626', linewidth=1.2)
    ax.add_patch(box5)
    ax.text(8.5, 4.0, "Air-Gapped Sovereign\nFastAPI Dashboard", ha='center', va='center', fontsize=8, fontweight='bold', color='#991b1b')
    ax.annotate('', xy=(6.9, 3.2), xytext=(7.2, 3.9),
                arrowprops=dict(arrowstyle="->", color='#b91c1c', lw=1.5))

    out_path = os.path.join(assets_dir, "spectra_callout_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

# -------------------------------------------------------------
# 2. Slide 3 Flow Chart (Tailored to SPECTRA NTRO Signal Pipeline)
# -------------------------------------------------------------
def create_flowchart_diagram():
    fig, ax = plt.subplots(figsize=(8.0, 4.5), dpi=300)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Primary Inputs & Fallback column (Left)
    b1 = patches.FancyBboxPatch((0.5, 4.2), 1.6, 1.0, boxstyle="square,pad=0",
                                facecolor='#fee2e2', edgecolor='#ef4444', linewidth=1.8)
    ax.add_patch(b1)
    ax.text(1.3, 4.7, "Raw .IQ\n& .wav Baseband", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#991b1b')

    b2 = patches.FancyBboxPatch((0.5, 2.5), 1.6, 1.0, boxstyle="square,pad=0",
                                facecolor='#ccfbf1', edgecolor='#14b8a6', linewidth=1.8)
    ax.add_patch(b2)
    ax.text(1.3, 3.0, "Welch PSD &\n4096-pt FFT", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0f766e')

    b3 = patches.FancyBboxPatch((0.5, 0.8), 1.6, 1.0, boxstyle="square,pad=0",
                                facecolor='#e0e7ff', edgecolor='#6366f1', linewidth=1.8)
    ax.add_patch(b3)
    ax.text(1.3, 1.3, "GF(2) Blind\nInterleaver", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#3730a3')

    # Center Output Box: NTRO SIGINT
    b_pnt = patches.FancyBboxPatch((2.7, 3.4), 1.25, 0.7, boxstyle="square,pad=0",
                                  facecolor='#a7f3d0', edgecolor='#10b981', linewidth=1.8)
    ax.add_patch(b_pnt)
    ax.text(3.32, 3.75, "NTRO SIGINT", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065f46')

    # Connectors between left boxes
    ax.annotate('', xy=(1.3, 3.5), xytext=(1.3, 4.2), arrowprops=dict(arrowstyle="->", color='#ef4444', lw=1.5))
    ax.text(1.35, 3.85, "No Sync", color='#ef4444', fontsize=6.5, fontweight='bold')

    ax.annotate('', xy=(1.3, 1.8), xytext=(1.3, 2.5), arrowprops=dict(arrowstyle="->", color='#14b8a6', lw=1.5))
    ax.text(1.35, 2.15, "Low SNR", color='#0f766e', fontsize=6.5, fontweight='bold')

    # Left to SIGINT arrows
    ax.annotate('', xy=(2.7, 3.75), xytext=(2.1, 4.7), arrowprops=dict(arrowstyle="->", color='#10b981', lw=1.5))
    ax.annotate('', xy=(2.7, 3.75), xytext=(2.1, 3.0), arrowprops=dict(arrowstyle="->", color='#10b981', lw=1.5))
    ax.annotate('', xy=(2.7, 3.75), xytext=(2.1, 1.3), arrowprops=dict(arrowstyle="->", color='#10b981', lw=1.5))

    # Right Upper Processing Chain: Cyclostationary Estimation
    sb1 = patches.FancyBboxPatch((4.5, 4.4), 1.5, 0.65, boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='#99f6e4', edgecolor='#0d9488', linewidth=1.2)
    ax.add_patch(sb1)
    ax.text(5.25, 4.72, "Carrier & CFO\nPeak Tracking", ha='center', va='center', fontsize=7, color='#115e59')

    sb2 = patches.FancyBboxPatch((6.3, 4.4), 1.5, 0.65, boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='#99f6e4', edgecolor='#0d9488', linewidth=1.2)
    ax.add_patch(sb2)
    ax.text(7.05, 4.72, "Cyclostationary\nSquaring Loop", ha='center', va='center', fontsize=7, color='#115e59')

    sb3 = patches.FancyBboxPatch((8.1, 4.4), 1.5, 0.65, boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor='#99f6e4', edgecolor='#0d9488', linewidth=1.2)
    ax.add_patch(sb3)
    ax.text(8.85, 4.72, "RRC Matched\nFilter & DDC", ha='center', va='center', fontsize=7, color='#115e59')

    ax.annotate('', xy=(6.3, 4.72), xytext=(6.0, 4.72), arrowprops=dict(arrowstyle="->", color='#0d9488', lw=1.2))
    ax.annotate('', xy=(8.1, 4.72), xytext=(7.8, 4.72), arrowprops=dict(arrowstyle="->", color='#0d9488', lw=1.2))

    # Lower Processing Chain (Adaptive Signal Processing)
    ap1 = patches.FancyBboxPatch((4.5, 3.2), 2.2, 0.5, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor='#fbcfe8', edgecolor='#db2777', linewidth=1.2)
    ax.add_patch(ap1)
    ax.text(5.6, 3.45, "Higher-Order Cumulants (C40, C63)", ha='center', va='center', fontsize=7, color='#831843')

    ap2 = patches.FancyBboxPatch((4.5, 2.4), 2.2, 0.5, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor='#fbcfe8', edgecolor='#db2777', linewidth=1.2)
    ax.add_patch(ap2)
    ax.text(5.6, 2.65, "Costas Loop & Gardner TED", ha='center', va='center', fontsize=7, color='#831843')

    ap3 = patches.FancyBboxPatch((4.5, 1.6), 2.2, 0.5, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor='#fbcfe8', edgecolor='#db2777', linewidth=1.2)
    ax.add_patch(ap3)
    ax.text(5.6, 1.85, "Galois Field GF(2) Matrix Rank", ha='center', va='center', fontsize=7, color='#831843')

    ap4 = patches.FancyBboxPatch((4.5, 0.8), 2.2, 0.5, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor='#fbcfe8', edgecolor='#db2777', linewidth=1.2)
    ax.add_patch(ap4)
    ax.text(5.6, 1.05, "Viterbi, RS & LDPC Decoders", ha='center', va='center', fontsize=7, color='#831843')

    # Flow arrows down
    ax.annotate('', xy=(5.6, 2.9), xytext=(5.6, 3.2), arrowprops=dict(arrowstyle="->", color='#db2777', lw=1.2))
    ax.annotate('', xy=(5.6, 2.1), xytext=(5.6, 2.4), arrowprops=dict(arrowstyle="->", color='#db2777', lw=1.2))
    ax.annotate('', xy=(5.6, 1.3), xytext=(5.6, 1.6), arrowprops=dict(arrowstyle="->", color='#db2777', lw=1.2))

    # ESP32 HIL Testbench & Anomaly Rejector
    sec_box = patches.FancyBboxPatch((7.2, 1.8), 2.4, 1.4, boxstyle="round,pad=0.08,rounding_size=0.15",
                                     facecolor='#fce7f3', edgecolor='#be185d', linewidth=1.5)
    ax.add_patch(sec_box)
    ax.text(8.4, 2.5, "ESP32 USB HIL\nTestbench & Anomaly Filter", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#9d174d')

    ax.annotate('', xy=(6.7, 2.5), xytext=(7.2, 2.5), arrowprops=dict(arrowstyle="->", color='#be185d', lw=1.5))
    ax.annotate('', xy=(8.4, 3.2), xytext=(8.4, 4.4), arrowprops=dict(arrowstyle="->", color='#0d9488', lw=1.2))

    # Connect upper to lower chain
    ax.plot([4.2, 4.2, 4.5], [4.7, 3.45, 3.45], color='#64748b', lw=1.2, linestyle='--')
    ax.plot([2.1, 4.5], [4.7, 4.7], color='#64748b', lw=1.2, linestyle=':')

    # Section Headers
    ax.text(1.3, 5.5, "SIGNAL INGESTION", ha='center', fontsize=8, fontweight='bold', color='#1e293b')
    ax.text(6.8, 5.5, "CYCLOSTATIONARY ESTIMATION", ha='center', fontsize=8, fontweight='bold', color='#0f766e')
    ax.text(5.6, 3.85, "ADAPTIVE COGNITIVE DEMODULATION", ha='center', fontsize=7.5, fontweight='bold', color='#be185d')

    out_path = os.path.join(assets_dir, "spectra_pipeline_flowchart.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

# -------------------------------------------------------------
# 3. Slide 3: 3-Layer Approach Block Diagram
# -------------------------------------------------------------
def create_3layer_approach_diagram():
    fig, ax = plt.subplots(figsize=(4.2, 2.2), dpi=300)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 3)
    ax.axis('off')

    # Draw 3 stacked 3D-perspective blocks
    l1 = patches.FancyBboxPatch((0.2, 0.2), 3.0, 0.65, boxstyle="square,pad=0",
                                facecolor='#fee2e2', edgecolor='#ef4444', linewidth=1.5)
    ax.add_patch(l1)
    ax.text(1.7, 0.52, "Layer 1: Baseband DSP & Conditioning", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#991b1b')
    ax.annotate('', xy=(3.3, 0.52), xytext=(4.15, 0.52), arrowprops=dict(arrowstyle="<-", color='#ef4444', lw=1.5))
    ax.text(4.2, 0.52, "RAW IQ", va='center', fontsize=7, fontweight='bold', color='#ef4444')

    l2 = patches.FancyBboxPatch((0.5, 1.0), 3.0, 0.65, boxstyle="square,pad=0",
                                facecolor='#ccfbf1', edgecolor='#14b8a6', linewidth=1.5)
    ax.add_patch(l2)
    ax.text(2.0, 1.32, "Layer 2: Feature Extraction & AMC", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#0f766e')
    ax.annotate('', xy=(3.6, 1.32), xytext=(4.15, 1.32), arrowprops=dict(arrowstyle="<-", color='#14b8a6', lw=1.5))
    ax.text(4.2, 1.32, "MOD/BAUD", va='center', fontsize=6.8, fontweight='bold', color='#0f766e')

    l3 = patches.FancyBboxPatch((0.8, 1.8), 3.0, 0.65, boxstyle="square,pad=0",
                                facecolor='#e0e7ff', edgecolor='#6366f1', linewidth=1.5)
    ax.add_patch(l3)
    ax.text(2.3, 2.12, "Layer 3: Blind Demod & GF(2) FEC", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#3730a3')
    ax.annotate('', xy=(3.9, 2.12), xytext=(4.15, 2.12), arrowprops=dict(arrowstyle="<-", color='#6366f1', lw=1.5))
    ax.text(4.2, 2.12, "DECODE", va='center', fontsize=7, fontweight='bold', color='#4338ca')

    ax.text(0.2, 2.7, "3 LAYER APPROACH", fontsize=8.5, fontweight='bold', color='#1e3a8a')

    out_path = os.path.join(assets_dir, "spectra_3layer_approach.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

# -------------------------------------------------------------
# 4. Slide 5: Uncharacterized RF Intercepts Trend Chart
# -------------------------------------------------------------
def create_jamming_trend_chart():
    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=300)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')

    years = ['2021', '2022', '2023', '2024', '2025', '2026 (Est)']
    volume_gb = [1200, 2800, 5400, 8900, 12400, 16500]

    bars = ax.bar(years, volume_gb, color='#38bdf8', edgecolor='#0284c7', width=0.6, linewidth=1.2)
    bars[-2].set_color('#0284c7')
    bars[-1].set_color('#ef4444')
    bars[-1].set_edgecolor('#b91c1c')

    ax.set_title("Uncharacterized RF Intercepts in Strategic Sectors\n(Monthly Ingested Volume in GB)", fontsize=8.5, fontweight='bold', color='#0f172a', pad=8)
    ax.set_ylabel("Monthly Ingested Data (GB)", fontsize=7.5, color='#475569')
    ax.tick_params(axis='both', which='major', labelsize=7, colors='#475569')
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='#94a3b8')

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color('#cbd5e1')
    ax.spines['bottom'].set_color('#cbd5e1')

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 300, f'{int(h):,}', ha='center', va='bottom', fontsize=6.2, fontweight='bold', color='#1e293b')

    out_path = os.path.join(assets_dir, "spectra_jamming_trend_chart.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Created: {out_path}")

if __name__ == "__main__":
    create_callout_diagram()
    create_flowchart_diagram()
    create_3layer_approach_diagram()
    create_jamming_trend_chart()
    print("All diagram assets successfully regenerated for SPECTRA.")
