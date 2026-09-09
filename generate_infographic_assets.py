import os
import matplotlib.pyplot as plt
import numpy as np

out_dir = r"C:\Users\Harik\.gemini\antigravity-ide\brain\218e3fa8-15eb-40a0-9f59-04745317229e"

def create_survey_donut_charts():
    """Generate professional side-by-side donut charts for Slide 6 Market Validation."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.8), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')

    # Palette
    color_yes = '#166534'   # Forest Green
    color_no = '#E2E8F0'    # Light Slate
    color_yes2 = '#1E40AF'  # Royal Navy Blue

    # Chart 1: Volatility Impact
    sizes1 = [94, 6]
    wedges1, texts1 = ax1.pie(sizes1, colors=[color_yes2, color_no], startangle=90, 
                               wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2))
    ax1.set_title("Does Spot Volatility Hurt\nProcurement Margins?", fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax1.text(0, 0, "94%\nYES", ha='center', va='center', fontsize=15, fontweight='bold', color=color_yes2)

    # Legend 1
    ax1.legend(["Agree / Impacted (94%)", "Unaffected (6%)"], loc="lower center", bbox_to_anchor=(0.5, -0.22), 
               frameon=False, fontsize=8.5)

    # Chart 2: Automated Draft & Congestion Prevention
    sizes2 = [91, 9]
    wedges2, texts2 = ax2.pie(sizes2, colors=[color_yes, color_no], startangle=90, 
                               wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2))
    ax2.set_title("Would Dynamic Draft &\nCongestion Alerts Cut Demurrage?", fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax2.text(0, 0, "91%\nYES", ha='center', va='center', fontsize=15, fontweight='bold', color=color_yes)

    # Legend 2
    ax2.legend(["High Demand (91%)", "Neutral (9%)"], loc="lower center", bbox_to_anchor=(0.5, -0.22), 
               frameon=False, fontsize=8.5)

    plt.tight_layout()
    chart_path = os.path.join(out_dir, "sih_survey_charts.png")
    plt.savefig(chart_path, dpi=200, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"Saved survey charts to: {chart_path}")

def create_project_dp_badge():
    """Generate a high-res circular Team / Project DP badge for Slide 1."""
    fig, ax = plt.subplots(figsize=(4.0, 4.0), dpi=250)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_aspect('equal')
    ax.axis('off')

    # Outer decorative rings
    ring_outer = plt.Circle((0.5, 0.5), 0.47, color='#1E3A8A', ec='#3B82F6', lw=3.5)
    ring_middle = plt.Circle((0.5, 0.5), 0.44, color='#0F172A', ec='#60A5FA', lw=1.5)
    ring_inner = plt.Circle((0.5, 0.5), 0.38, color='#1E293B', ec='#93C5FD', lw=1.0)
    ax.add_patch(ring_outer)
    ax.add_patch(ring_middle)
    ax.add_patch(ring_inner)

    # Central Maritime Icon / Wave / Ship geometry
    # Vessel hull
    hull_x = [0.28, 0.72, 0.65, 0.35]
    hull_y = [0.44, 0.44, 0.34, 0.34]
    ax.fill(hull_x, hull_y, color='#38BDF8', ec='#E0F2FE', lw=1.5)

    # Containers on deck
    ax.fill([0.34, 0.45, 0.45, 0.34], [0.44, 0.44, 0.52, 0.52], color='#F59E0B')
    ax.fill([0.47, 0.58, 0.58, 0.47], [0.44, 0.44, 0.54, 0.54], color='#10B981')
    ax.fill([0.60, 0.66, 0.66, 0.60], [0.44, 0.44, 0.50, 0.50], color='#EF4444')

    # Waves below hull
    wave_x = np.linspace(0.22, 0.78, 100)
    wave_y1 = 0.30 + 0.02 * np.sin(wave_x * 25)
    wave_y2 = 0.25 + 0.015 * np.sin(wave_x * 25 + 1)
    ax.plot(wave_x, wave_y1, color='#60A5FA', lw=2)
    ax.plot(wave_x, wave_y2, color='#38BDF8', lw=1.5)

    # Radar / AI Beam arc
    radar_theta = np.linspace(0, np.pi, 50)
    r_arc = 0.18
    ax.plot(0.5 + r_arc*np.cos(radar_theta), 0.54 + r_arc*np.sin(radar_theta)*0.6, color='#A7F3D0', lw=1.2, ls='--')

    # Typography inside badge
    ax.text(0.5, 0.68, "FREIGHTFORECAST PRO", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF')
    ax.text(0.5, 0.62, "AI MARITIME INTELLIGENCE", ha='center', va='center', fontsize=6.5, fontweight='bold', color='#38BDF8')
    
    # Bottom team tag
    ax.text(0.5, 0.18, "TEAM FUTURISTICS", ha='center', va='center', fontsize=8.0, fontweight='bold', color='#F59E0B')
    ax.text(0.5, 0.12, "SIH 2026 • FINAL ROUND", ha='center', va='center', fontsize=6.0, color='#94A3B8')

    plt.tight_layout()
    dp_path = os.path.join(out_dir, "project_dp_badge.png")
    plt.savefig(dp_path, dpi=250, bbox_inches='tight', facecolor='#FFFFFF', transparent=True)
    plt.close()
    print(f"Saved DP badge to: {dp_path}")

if __name__ == "__main__":
    create_survey_donut_charts()
    create_project_dp_badge()
