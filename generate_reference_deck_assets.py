import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"c:\vs studio\freight-forecast\sih_assets"
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. Slide 2: Center Device / System Mockup with Callouts
# -------------------------------------------------------------
def generate_slide2_center_mockup():
    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    
    # Draw central device/dashboard card
    card = patches.FancyBboxPatch((1.6, 1.2), 3.3, 2.6, boxstyle="round,pad=0.1,rounding_size=0.15",
                                  facecolor="#0F172A", edgecolor="#38BDF8", linewidth=2.5, zorder=2)
    ax.add_patch(card)
    
    # Internal screen area
    screen = patches.FancyBboxPatch((1.75, 1.45), 3.0, 2.1, boxstyle="round,pad=0.05,rounding_size=0.08",
                                    facecolor="#0B1329", edgecolor="#1E293B", linewidth=1.2, zorder=3)
    ax.add_patch(screen)
    
    # Mini chart inside screen (Holt Winters rate curve)
    x = np.linspace(1.9, 4.6, 40)
    y = 2.4 + 0.3 * np.sin(x * 3.5) - 0.15 * (x - 1.9)
    ax.plot(x, y, color="#38BDF8", lw=2.2, zorder=4)
    ax.fill_between(x, y - 0.15, y + 0.15, color="#0284C7", alpha=0.25, zorder=3)
    
    # Text inside screen
    ax.text(3.25, 3.25, "FREIGHTFORECAST PRO", color="#F8FAFC", fontsize=8.5, weight="bold", ha="center", zorder=5)
    ax.text(3.25, 3.05, "Capesize 90-Day Rate: $27,700/day", color="#34D399", fontsize=7.5, ha="center", zorder=5)
    ax.text(3.25, 1.65, "AIS Telematics Active | Port UKC: 1.82m SAFE", color="#94A3B8", fontsize=6.5, ha="center", zorder=5)
    
    # Mini ship icon / marker on screen
    ax.plot([2.5, 3.5, 4.1], [2.1, 2.0, 1.9], 'o', color="#F59E0B", markersize=4, zorder=5)
    
    # Callout boxes around device
    # Callout 1: Top Left
    c1 = patches.FancyBboxPatch((0.05, 3.8), 2.2, 0.7, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=1.2, zorder=6)
    ax.add_patch(c1)
    ax.text(1.15, 4.15, "Holt-Winters 90-Day\nRate Curve (1.7% MAPE)", color="#92400E", fontsize=7.5, weight="bold", ha="center", va="center", zorder=7)
    ax.annotate("", xy=(2.2, 2.7), xytext=(1.8, 3.8),
                arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.5, connectionstyle="arc3,rad=-0.15"), zorder=5)
    
    # Callout 2: Bottom Left
    c2 = patches.FancyBboxPatch((0.05, 0.5), 2.2, 0.7, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor="#E0E7FF", edgecolor="#6366F1", linewidth=1.2, zorder=6)
    ax.add_patch(c2)
    ax.text(1.15, 0.85, "Tidal Draught & UKC Solver\n(Haldia/Paradip Siltation)", color="#3730A3", fontsize=7.5, weight="bold", ha="center", va="center", zorder=7)
    ax.annotate("", xy=(2.0, 1.55), xytext=(1.8, 1.2),
                arrowprops=dict(arrowstyle="->", color="#4F46E5", lw=1.5, connectionstyle="arc3,rad=0.15"), zorder=5)

    # Callout 3: Top Right
    c3 = patches.FancyBboxPatch((4.25, 3.8), 2.2, 0.7, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor="#E0F2FE", edgecolor="#0284C7", linewidth=1.2, zorder=6)
    ax.add_patch(c3)
    ax.text(5.35, 4.15, "Satellite AIS Telematics\n& Port Congestion GIS", color="#0369A1", fontsize=7.5, weight="bold", ha="center", va="center", zorder=7)
    ax.annotate("", xy=(4.3, 2.7), xytext=(4.7, 3.8),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5, connectionstyle="arc3,rad=0.15"), zorder=5)

    # Callout 4: Bottom Right
    c4 = patches.FancyBboxPatch((4.25, 0.5), 2.2, 0.7, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor="#FEE2E2", edgecolor="#EF4444", linewidth=1.2, zorder=6)
    ax.add_patch(c4)
    ax.text(5.35, 0.85, "Spot vs Forward Hedging\n(₹28.4 Cr Program Savings)", color="#991B1B", fontsize=7.5, weight="bold", ha="center", va="center", zorder=7)
    ax.annotate("", xy=(4.5, 1.55), xytext=(4.7, 1.2),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5, connectionstyle="arc3,rad=-0.15"), zorder=5)

    # Callout 5: Bottom Center
    c5 = patches.FancyBboxPatch((2.2, 0.05), 2.1, 0.5, boxstyle="round,pad=0.05,rounding_size=0.08",
                                facecolor="#D1FAE5", edgecolor="#10B981", linewidth=1.2, zorder=6)
    ax.add_patch(c5)
    ax.text(3.25, 0.3, "Sub-35ms In-Memory Redis Engine", color="#065F46", fontsize=7.5, weight="bold", ha="center", va="center", zorder=7)
    ax.annotate("", xy=(3.25, 1.2), xytext=(3.25, 0.55),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5), zorder=5)

    ax.set_xlim(-0.1, 6.6)
    ax.set_ylim(-0.1, 4.8)
    ax.axis("off")
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "ref_slide2_center_mockup.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Generated:", out_path)

# -------------------------------------------------------------
# 2. Slide 3: Flowchart & 3-Layer Approach
# -------------------------------------------------------------
def generate_slide3_flowchart():
    fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    
    # Ingestion Block (Left, Red/Orange)
    b_ingest = patches.FancyBboxPatch((0.2, 1.8), 1.5, 1.4, boxstyle="round,pad=0.05,rounding_size=0.08",
                                      facecolor="#FEE2E2", edgecolor="#EF4444", linewidth=1.5, zorder=2)
    ax.add_patch(b_ingest)
    ax.text(0.95, 2.5, "Baltic Index\n&\nAIS Stream", color="#991B1B", fontsize=8.5, weight="bold", ha="center", va="center", zorder=3)
    
    # Fallback / secondary block
    b_tides = patches.FancyBboxPatch((0.2, 0.4), 1.5, 1.0, boxstyle="round,pad=0.05,rounding_size=0.08",
                                     facecolor="#E0E7FF", edgecolor="#6366F1", linewidth=1.5, zorder=2)
    ax.add_patch(b_tides)
    ax.text(0.95, 0.9, "Port Trust\nTidal Circulars", color="#3730A3", fontsize=8.0, weight="bold", ha="center", va="center", zorder=3)
    
    # Middle Processing Block 1 (Cyan/Teal)
    b_p1 = patches.FancyBboxPatch((2.2, 2.7), 1.7, 0.8, boxstyle="round,pad=0.05,rounding_size=0.08",
                                  facecolor="#CCFBF1", edgecolor="#14B8A6", linewidth=1.5, zorder=2)
    ax.add_patch(b_p1)
    ax.text(3.05, 3.1, "Data Harmonization\n& Normalization", color="#0F766E", fontsize=7.5, weight="bold", ha="center", va="center", zorder=3)

    # Middle Processing Block 2 (Green)
    b_p2 = patches.FancyBboxPatch((2.2, 1.6), 1.7, 0.8, boxstyle="round,pad=0.05,rounding_size=0.08",
                                  facecolor="#D1FAE5", edgecolor="#10B981", linewidth=1.5, zorder=2)
    ax.add_patch(b_p2)
    ax.text(3.05, 2.0, "Holt-Winters Core\n(Decomposition)", color="#065F46", fontsize=7.5, weight="bold", ha="center", va="center", zorder=3)

    # Middle Processing Block 3 (Pink)
    b_p3 = patches.FancyBboxPatch((2.2, 0.5), 1.7, 0.8, boxstyle="round,pad=0.05,rounding_size=0.08",
                                  facecolor="#FCE7F3", edgecolor="#EC4899", linewidth=1.5, zorder=2)
    ax.add_patch(b_p3)
    ax.text(3.05, 0.9, "SciPy UKC Solver\n(Tidal Berth Intake)", color="#9D174D", fontsize=7.5, weight="bold", ha="center", va="center", zorder=3)

    # Right Pipeline Blocks (Cyan / Purple)
    b_r1 = patches.FancyBboxPatch((4.4, 2.7), 2.0, 0.8, boxstyle="round,pad=0.05,rounding_size=0.08",
                                  facecolor="#E0F2FE", edgecolor="#0284C7", linewidth=1.5, zorder=2)
    ax.add_patch(b_r1)
    ax.text(5.4, 3.1, "10k Monte Carlo\nVolatility Bounds", color="#0369A1", fontsize=7.5, weight="bold", ha="center", va="center", zorder=3)

    b_r2 = patches.FancyBboxPatch((4.4, 1.6), 2.0, 0.8, boxstyle="round,pad=0.05,rounding_size=0.08",
                                  facecolor="#EDE9FE", edgecolor="#8B5CF6", linewidth=1.5, zorder=2)
    ax.add_patch(b_r2)
    ax.text(5.4, 2.0, "Market Entry Score\n& Demurrage Shield", color="#5B21B6", fontsize=7.5, weight="bold", ha="center", va="center", zorder=3)

    b_r3 = patches.FancyBboxPatch((4.4, 0.5), 2.0, 0.8, boxstyle="round,pad=0.05,rounding_size=0.08",
                                  facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=1.5, zorder=2)
    ax.add_patch(b_r3)
    ax.text(5.4, 0.9, "Decision Output:\nSpot vs COA Hedge", color="#92400E", fontsize=7.5, weight="bold", ha="center", va="center", zorder=3)

    # Arrows
    arrow_kw = dict(arrowstyle="->", color="#64748B", lw=1.4)
    ax.annotate("", xy=(2.2, 3.1), xytext=(1.7, 2.7), arrowprops=arrow_kw)
    ax.annotate("", xy=(2.2, 2.0), xytext=(1.7, 2.4), arrowprops=arrow_kw)
    ax.annotate("", xy=(2.2, 0.9), xytext=(1.7, 0.9), arrowprops=arrow_kw)
    ax.annotate("", xy=(4.4, 3.1), xytext=(3.9, 3.1), arrowprops=arrow_kw)
    ax.annotate("", xy=(4.4, 2.0), xytext=(3.9, 2.0), arrowprops=arrow_kw)
    ax.annotate("", xy=(4.4, 0.9), xytext=(3.9, 0.9), arrowprops=arrow_kw)

    # Top indicator pill
    pill = patches.FancyBboxPatch((2.2, 3.55), 2.4, 0.22, boxstyle="round,pad=0.02,rounding_size=0.05",
                                  facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=0.8, zorder=2)
    ax.add_patch(pill)
    ax.text(3.4, 3.66, "Continuous Real-Time Processing", color="#475569", fontsize=6.5, ha="center", va="center", zorder=3)

    ax.set_xlim(0, 6.7)
    ax.set_ylim(0.2, 3.9)
    ax.axis("off")
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "ref_slide3_flowchart.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Generated:", out_path)

def generate_slide3_3layer_graphic():
    fig, ax = plt.subplots(figsize=(3.4, 1.8), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    
    # 3 Layer stacked block graphic matching reference
    # Layer 1: Bottom (Green)
    b1 = patches.Rectangle((0.1, 0.1), 3.0, 0.45, facecolor="#10B981", edgecolor="#059669", linewidth=1.2, zorder=2)
    ax.add_patch(b1)
    ax.text(1.6, 0.325, "Layer 1: Data Ingestion (Baltic / AIS / Tides)", color="#FFFFFF", fontsize=6.5, weight="bold", ha="center", va="center", zorder=3)

    # Layer 2: Middle (Red/Coral)
    b2 = patches.Rectangle((0.25, 0.65), 2.8, 0.45, facecolor="#EF4444", edgecolor="#DC2626", linewidth=1.2, zorder=2)
    ax.add_patch(b2)
    ax.text(1.65, 0.875, "Layer 2: AI Forecasting & Draught Solver", color="#FFFFFF", fontsize=6.5, weight="bold", ha="center", va="center", zorder=3)

    # Layer 3: Top (Dark Navy)
    b3 = patches.Rectangle((0.4, 1.2), 2.6, 0.45, facecolor="#0F172A", edgecolor="#38BDF8", linewidth=1.2, zorder=2)
    ax.add_patch(b3)
    ax.text(1.7, 1.425, "Layer 3: Decision & Demurrage Shield", color="#38BDF8", fontsize=6.5, weight="bold", ha="center", va="center", zorder=3)

    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 1.8)
    ax.axis("off")
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "ref_slide3_3layer.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Generated:", out_path)

# -------------------------------------------------------------
# 3. Slide 5: Bar Chart (Demurrage & Logistics Savings in India)
# -------------------------------------------------------------
def generate_slide5_barchart():
    fig, ax = plt.subplots(figsize=(4.8, 3.0), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    
    years = ["2024", "2025", "2026", "2027", "2028"]
    savings = [850, 1650, 3100, 4800, 6200]
    colors = ["#38BDF8", "#0284C7", "#0369A1", "#0284C7", "#00A896"]
    
    bars = ax.bar(years, savings, width=0.55, color=colors, edgecolor="#0F172A", linewidth=0.8, zorder=3)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"₹{height} Cr",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=7.5, weight="bold", color="#0F172A")
        
    ax.set_title("Projected Demurrage & Logistics Savings in India", fontsize=9.0, weight="bold", color="#0F172A", pad=12)
    ax.set_ylabel("Savings (₹ in Crores)", fontsize=7.5, weight="bold", color="#475569")
    ax.set_xlabel("Year", fontsize=7.5, weight="bold", color="#475569")
    ax.set_ylim(0, 7200)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=1)
    ax.tick_params(axis="both", labelsize=7.5, colors="#475569")
    
    # Hide top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "ref_slide5_barchart.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("Generated:", out_path)

if __name__ == "__main__":
    generate_slide2_center_mockup()
    generate_slide3_flowchart()
    generate_slide3_3layer_graphic()
    generate_slide5_barchart()
