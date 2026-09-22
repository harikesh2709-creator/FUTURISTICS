import re

html_path = r'c:\vs studio\ntro-signal-analyzer\frontend\sih_presentation.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace image paths
replacements = {
    'presentation_assets/screen_constellation.png': 'presentation_assets/crop_constellation_clean.png',
    'presentation_assets/screen_neural_lab.png': 'presentation_assets/crop_neural_amc_clean.png',
    'presentation_assets/screen_risk_console.png': 'presentation_assets/crop_risk_spectral_anomaly.png',
    'presentation_assets/screen_interleaver_solver.png': 'presentation_assets/crop_interleaver_hex_clean.png',
    'presentation_assets/screen_ground_truth.png': 'presentation_assets/crop_ground_truth_clean.png',
}

# In slide 7, module 1 should be crop_module1_telemetry.png, and module 2 should be crop_module2_neural_lab.png
content = content.replace('<img src="presentation_assets/screen_mission_radar.png" alt="Module 1"', '<img src="presentation_assets/crop_module1_telemetry.png" alt="Module 1"')
# Note: screen_neural_lab.png in slide 7 module 2
content = re.sub(r'<img src="presentation_assets/screen_neural_lab\.png" alt="Module 2"', '<img src="presentation_assets/crop_module2_neural_lab.png" alt="Module 2"', content)

for old, new in replacements.items():
    content = content.replace(old, new)

# Update font sizes in CSS
content = content.replace('.header-title-box .main { color: var(--navy-dark); font-weight: 800; font-size: 18.5px;', '.header-title-box .main { color: var(--navy-dark); font-weight: 800; font-size: 21px;')
content = content.replace('.card-ribbon {', '.card-ribbon {\n      font-size: 11px;\n      font-weight: 800;')
content = content.replace('table.custom-table { width: 100%; border-collapse: collapse; font-size: 10.5px; }', 'table.custom-table { width: 100%; border-collapse: collapse; font-size: 11px; }')
content = content.replace('table.custom-table th { background: var(--navy-pill); color: var(--cyan-accent); padding: 5px 8px; text-align: left; font-weight: 700; font-size: 10px; }', 'table.custom-table th { background: var(--navy-pill); color: var(--cyan-accent); padding: 6px 8px; text-align: left; font-weight: 800; font-size: 11px; }')
content = content.replace('.stat-val { font-size: 20px; font-weight: 900; line-height: 1.1; margin-bottom: 2px; }', '.stat-val { font-size: 25px; font-weight: 900; line-height: 1.1; margin-bottom: 3px; }')
content = content.replace('.stat-label { font-size: 10px; font-weight: 800; color: var(--navy-dark); }', '.stat-label { font-size: 11.5px; font-weight: 800; color: var(--navy-dark); }')

# Slide 1 font size bumps
content = content.replace('font-size:13px; line-height:1.4;', 'font-size:14.5px; line-height:1.45;')
content = content.replace('min-width:185px;', 'min-width:205px;')
content = content.replace('font-size:26px;', 'font-size:30px;')

# Save updated file
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated sih_presentation.html with clean cropped assets and larger font sizes!")
