import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

assets_dir = r'c:\vs studio\ntro-signal-analyzer\presentation_assets'
os.makedirs(assets_dir, exist_ok=True)
out_path = os.path.join(assets_dir, 'system_architecture_3s_puredsp.png')

fig, ax = plt.subplots(figsize=(11, 4.5), dpi=300)
fig.patch.set_facecolor('#0B192C')
ax.set_facecolor('#0B192C')
ax.axis('off')
ax.set_xlim(0, 11)
ax.set_ylim(0, 4.5)

# Color tokens
c_navy = '#0F172A'
c_cyan = '#0EA5E9'
c_blue = '#2563EB'
c_purple = '#7C3AED'
c_emerald = '#10B981'
c_amber = '#F59E0B'
c_text_bright = '#F8FAFC'
c_text_sub = '#94A3B8'
c_border = '#334155'

# Title
ax.text(5.5, 4.2, "SPECTRA DETERMINISTIC 3S DSP SYSTEM ARCHITECTURE", 
        fontsize=13, fontweight='bold', color=c_cyan, ha='center', va='center', family='sans-serif')
ax.text(5.5, 3.85, "1. STRUCTURED INGESTION  ──►  2. MATHEMATICAL DSP & STATISTICAL INFERENCE  ──►  3. SOVEREIGN ACTION",
        fontsize=8.5, fontweight='bold', color='#CBD5E1', ha='center', va='center', family='sans-serif')

# Box 1: S1 - STRUCTURED INGESTION
b1 = patches.FancyBboxPatch((0.4, 0.4), 3.0, 3.1, boxstyle="round,pad=0.1",
                            facecolor=c_navy, edgecolor=c_blue, linewidth=1.8)
ax.add_patch(b1)
ax.text(1.9, 3.25, "STAGE 1: STRUCTURED INGESTION", fontsize=9.5, fontweight='bold', color='#60A5FA', ha='center', family='sans-serif')
ax.plot([0.6, 3.2], [3.05, 3.05], color=c_border, linewidth=1)

s1_items = [
    "• Raw .IQ (Float32 / Int16)",
    "• Spacecraft Telemetry .wav",
    "• SDR Stream (USRP / HackRF)",
    "• Polyphase Decimation Filter",
    "• Automated DC Offset Nulling",
    "• Quadrature I/Q Gain Balancing"
]
for i, item in enumerate(s1_items):
    ax.text(0.65, 2.75 - i*0.42, item, fontsize=8.2, color=c_text_bright, va='center', family='sans-serif')

# Arrow 1 -> 2
ax.annotate("", xy=(3.9, 1.95), xytext=(3.5, 1.95),
            arrowprops=dict(arrowstyle="->", color=c_cyan, lw=2.5))

# Box 2: S2 - DETERMINISTIC DSP & PARAMETER EXTRACTION (NO AI)
b2 = patches.FancyBboxPatch((4.0, 0.4), 3.4, 3.1, boxstyle="round,pad=0.1",
                            facecolor=c_navy, edgecolor=c_purple, linewidth=1.8)
ax.add_patch(b2)
ax.text(5.7, 3.25, "STAGE 2: DETERMINISTIC DSP ENGINE", fontsize=9.5, fontweight='bold', color='#C084FC', ha='center', family='sans-serif')
ax.plot([4.2, 7.2], [3.05, 3.05], color=c_border, linewidth=1)

s2_items = [
    "• Cyclostationary Sx^α(f) Lines",
    "• Higher-Order Cumulants (C40, C42)",
    "• Decision-Tree ML-AMC (<15ms)",
    "• Gardner Timing Error Detector (TED)",
    "• 4th-Power FFT & Costas Loop PLL",
    "• Galois Field GF(2) Matrix Rank Solver"
]
for i, item in enumerate(s2_items):
    ax.text(4.25, 2.75 - i*0.42, item, fontsize=8.2, color=c_text_bright, va='center', family='sans-serif')

# Arrow 2 -> 3
ax.annotate("", xy=(7.9, 1.95), xytext=(7.5, 1.95),
            arrowprops=dict(arrowstyle="->", color=c_emerald, lw=2.5))

# Box 3: S3 - SOVEREIGN C4ISR ACTION
b3 = patches.FancyBboxPatch((8.0, 0.4), 2.6, 3.1, boxstyle="round,pad=0.1",
                            facecolor=c_navy, edgecolor=c_emerald, linewidth=1.8)
ax.add_patch(b3)
ax.text(9.3, 3.25, "STAGE 3: SOVEREIGN ACTION", fontsize=9.5, fontweight='bold', color='#34D399', ha='center', family='sans-serif')
ax.plot([8.2, 10.4], [3.05, 3.05], color=c_border, linewidth=1)

s3_items = [
    "• Recovered Payload Bitstream",
    "• Hard-Decision Viterbi Trellis",
    "• WebGL Constellation & PSD",
    "• SHA-256 Telemetry Dossier",
    "• Doppler & Orbit Ephemeris Sync",
    "• 100% Air-Gapped Sovereign Ops"
]
for i, item in enumerate(s3_items):
    ax.text(8.25, 2.75 - i*0.42, item, fontsize=8.2, color=c_text_bright, va='center', family='sans-serif')

plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"Generated Pure DSP 3S architecture image at: {out_path}")
