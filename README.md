# 🚢 Freight Forecast Pro — SIH 2026

**AI-Driven Freight Rate Forecasting & Multi-Modal Logistics Intelligence Platform**  
*Developed for Smart India Hackathon (SIH 2026)*

---

## 🌟 Overview

**Freight Forecast Pro** is an advanced maritime and multi-modal logistics intelligence suite engineered to predict ocean freight rates, optimize shipping corridors, and mitigate supply chain disruptions using machine learning and real-time telemetry.

### Key Capabilities

- **Real-Time Freight Forecasting**: Predictive engine analyzing bunker fuel prices, port congestion indices, seasonality, and geopolitical trade lane risks.
- **Dynamic WebSocket Telemetry Server**: High-throughput live tracking server broadcasting container updates, vessel coordinates, and automated disruption alerts.
- **Interactive Command Center**: Glassmorphic UI dashboard featuring live vessel tracking, dynamic pricing charts, carbon footprint calculator, and port status monitors.
- **Automated Presentation Engine**: Programmatic deck and report generators for hackathon evaluations and MSME stakeholders.

---

## 📁 Repository Structure

```
freight-forecast/
├── css/                        # Responsive CSS styles and design system
├── js/                         # Frontend charting, WebSocket logic, map integration
├── server/
│   ├── ws_server.py            # Live WebSocket server for real-time telemetry
│   ├── run_server.py           # Server bootstrap runner
│   ├── test_ws.py              # WebSocket connection test client
│   └── requirements.txt        # Backend dependencies
├── index.html                  # Main operational dashboard interface
├── presentation.html           # Interactive HTML slide deck for SIH pitch
├── SIH2026_FreightForecast_Pro.pptx # Official PowerPoint presentation deck
├── SIH2026_FreightForecast_Pro.pdf  # Compiled PDF pitch deck
├── build_champion_sih_deck.py  # Automation script for pitch deck compilation
├── generate_storm_style_deck.py# Storm visual style presentation builder
└── render_storm.py             # Headless slide renderer
```

---

## 🚀 Quick Start

### 1. Run the Operational Dashboard
Open `index.html` directly in any modern web browser or serve via a local HTTP server:
```bash
python -m http.server 8000
```
Navigate to `http://localhost:8000` to view the Freight Forecast Pro dashboard.

### 2. Start the Telemetry WebSocket Server
```bash
cd server
pip install -r requirements.txt
python ws_server.py
```

---

## 🔒 Confidentiality & License

This repository is proprietary and private to the creator for Smart India Hackathon (SIH 2026) innovation submission.
