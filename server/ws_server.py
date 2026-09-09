"""
FreightForecast Pro — Real-Time WebSocket Streaming Server
Broadcasts live AIS vessel telematics, spot freight rate ticks,
and high-priority port/weather risk alerts to connected dashboards.
"""

import asyncio
import json
import logging
import math
import random
import time
import os
from typing import Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ws_server")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="FreightForecast Pro Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Connection Manager ────────────────────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Active clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected. Active clients: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        payload = json.dumps(message)
        dead_connections = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                dead_connections.add(connection)
        for dead in dead_connections:
            self.active_connections.discard(dead)

manager = ConnectionManager()

# ── Maritime Domain Data ──────────────────────────────────────────────────────
ORIGIN_PORTS = [
    {"id": "newcastle", "name": "Newcastle", "country": "Australia", "coords": [-32.92, 151.78]},
    {"id": "haypoint", "name": "Hay Point", "country": "Australia", "coords": [-21.27, 149.30]},
    {"id": "richardsbay", "name": "Richards Bay", "country": "South Africa", "coords": [-28.79, 32.09]},
    {"id": "samarinda", "name": "Samarinda", "country": "Indonesia", "coords": [-0.50, 117.15]},
    {"id": "muara_pantai", "name": "Muara Pantai", "country": "Indonesia", "coords": [2.15, 117.65]},
]

DEST_PORTS = [
    {"id": "paradip", "name": "Paradip", "country": "India", "coords": [20.26, 86.67], "draftLimit": 14.5},
    {"id": "vizag", "name": "Visakhapatnam", "country": "India", "coords": [17.68, 83.27], "draftLimit": 18.1},
    {"id": "haldia", "name": "Haldia", "country": "India", "coords": [22.02, 88.06], "draftLimit": 8.5},
    {"id": "dhamra", "name": "Dhamra", "country": "India", "coords": [20.79, 86.96], "draftLimit": 17.5},
    {"id": "ennore", "name": "Kamarajar (Ennore)", "country": "India", "coords": [13.26, 80.33], "draftLimit": 16.0},
    {"id": "krishnapatnam", "name": "Krishnapatnam", "country": "India", "coords": [14.25, 80.12], "draftLimit": 18.5},
]

VESSEL_CLASSES = [
    {"class": "Capesize", "dwt": 180000, "speed": 13.5, "draft": 18.2, "prefix": "MV OCEAN"},
    {"class": "Panamax", "dwt": 75000, "speed": 14.0, "draft": 14.2, "prefix": "MV BHARAT"},
    {"class": "Supramax", "dwt": 58000, "speed": 14.2, "draft": 12.8, "prefix": "MV ASIA"},
    {"class": "Handysize", "dwt": 35000, "speed": 13.8, "draft": 10.5, "prefix": "MV EAST"}
]

# Generate Initial Active Fleet
FLEET = []
for i in range(24):
    v_class = random.choice(VESSEL_CLASSES)
    origin = random.choice(ORIGIN_PORTS)
    dest = random.choice(DEST_PORTS)
    progress = random.uniform(0.08, 0.92)
    imo = 9300000 + i * 173 + random.randint(100, 999)
    name = f"{v_class['prefix']} {['TITAN', 'GLORY', 'PIONEER', 'VICTORIA', 'VALIANT', 'FORTUNE', 'DRAGON', 'HARMONY', 'PRIDE', 'VOYAGER'][i % 10]}"
    
    status = "In Transit"
    if random.random() < 0.2:
        status = "Delayed (Weather)"
    elif random.random() < 0.15:
        status = "Anchorage Waiting"

    FLEET.append({
        "imo": str(imo),
        "name": name,
        "vesselClass": v_class["class"],
        "dwt": v_class["dwt"],
        "origin": origin,
        "dest": dest,
        "progress": progress,
        "speed": round(v_class["speed"] + random.uniform(-1.0, 1.2), 1),
        "heading": random.randint(280, 340),
        "draft": round(v_class["draft"] * random.uniform(0.92, 1.0), 1),
        "cargoMT": int(v_class["dwt"] * random.uniform(0.90, 0.98)),
        "status": status,
        "demurrageRiskUSD": 0 if status == "In Transit" else random.randint(12000, 48000)
    })

# Market Rates State
MARKET_RATES = {
    "CAPESIZE": {"rate": 24850, "delta": 0.0},
    "PANAMAX": {"rate": 15420, "delta": 0.0},
    "SUPRAMAX": {"rate": 13180, "delta": 0.0},
    "HANDYSIZE": {"rate": 10950, "delta": 0.0},
    "BDI": {"rate": 1845, "delta": 0.0},
    "BUNKER_VLSFO": {"rate": 585, "delta": 0.0}
}

RISK_TEMPLATES = [
    {"type": "weather", "severity": "warning", "title": "South Bay Monsoon Swell", "message": "Significant wave height 3.8m impacting passage east of Sri Lanka. Expected speed reduction: 1.5 kts."},
    {"type": "congestion", "severity": "critical", "title": "Paradip Anchorage Delay Exceeds 6 Days", "message": "High waiting times for Capesize berths. Recommended diversion or lightering at Dhamra."},
    {"type": "market", "severity": "info", "title": "Capesize Rate Surge", "message": "Spot iron ore fixture surge in WA-China corridor pushes Atlantic/Indian Ocean tonnage hire up 3.2%."},
    {"type": "draft", "severity": "warning", "title": "Haldia River Draft Advisory", "message": "Hooghly river siltation limits maximum permissible draft to 8.2m for spring tides."},
    {"type": "bunker", "severity": "info", "title": "Singapore Bunker Price Shift", "message": "VLSFO benchmark settled at $588/MT (+$6.50). Bunker recalculations applied to open voyages."}
]

# ── Endpoints & Static Files ──────────────────────────────────────────────────
@app.get("/")
async def serve_index():
    index_file = os.path.join(PROJECT_ROOT, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"service": "FreightForecast Pro", "status": "online"}

@app.get("/presentation")
async def serve_presentation():
    pres_file = os.path.join(PROJECT_ROOT, "presentation.html")
    if os.path.exists(pres_file):
        return FileResponse(pres_file)
    return {"error": "Presentation file not found"}

@app.get("/api/info")
def read_info():
    return {
        "service": "FreightForecast Pro WebSocket Server",
        "status": "online",
        "active_clients": len(manager.active_connections),
        "vessels_tracked": len(FLEET)
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "uptime": "operational",
        "timestamp": time.time(),
        "clients": len(manager.active_connections)
    }

# Mount static asset directories
if os.path.exists(os.path.join(PROJECT_ROOT, "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(PROJECT_ROOT, "css")), name="css")
if os.path.exists(os.path.join(PROJECT_ROOT, "js")):
    app.mount("/js", StaticFiles(directory=os.path.join(PROJECT_ROOT, "js")), name="js")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Send immediate state on connection
    welcome_packet = {
        "type": "INITIAL_STATE",
        "timestamp": time.time(),
        "fleet": FLEET,
        "rates": MARKET_RATES,
        "serverTime": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    }
    await websocket.send_text(json.dumps(welcome_packet))

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle heartbeat ping
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "clientTime": message.get("t"),
                    "serverTime": time.time()
                }))
            
            # Handle custom message or broadcast
            elif message.get("type") == "request_refresh":
                await websocket.send_text(json.dumps({
                    "type": "FLEET_UPDATE",
                    "fleet": FLEET,
                    "timestamp": time.time()
                }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# ── Background Streaming Tasks ────────────────────────────────────────────────
async def stream_telematics():
    """Update AIS vessel positions and broadcast every 2.5 seconds."""
    while True:
        await asyncio.sleep(2.5)
        if not manager.active_connections:
            continue

        for v in FLEET:
            if "Delayed" not in v["status"]:
                v["progress"] += 0.0008
                if v["progress"] >= 0.98:
                    v["progress"] = 0.05
                    # Switch route
                    v["origin"] = random.choice(ORIGIN_PORTS)
                    v["dest"] = random.choice(DEST_PORTS)

            # Interpolate coordinates
            o_lat, o_lng = v["origin"]["coords"]
            d_lat, d_lng = v["dest"]["coords"]
            
            # Slight curvature for nautical routing
            prog = v["progress"]
            current_lat = o_lat + (d_lat - o_lat) * prog
            current_lng = o_lng + (d_lng - o_lng) * prog
            # Add small realistic micro-variance
            v["lat"] = round(current_lat + math.sin(prog * math.pi) * 0.4, 4)
            v["lng"] = round(current_lng + math.cos(prog * math.pi) * 0.4, 4)

            # ETA calculation
            rem_dist = (1 - prog) * 4500
            v["etaDays"] = round(rem_dist / (v["speed"] * 24), 1)

        await manager.broadcast({
            "type": "TELEMATICS_UPDATE",
            "timestamp": time.time(),
            "fleet": FLEET
        })

async def stream_market_rates():
    """Simulate spot rate updates and BDI ticks every 5 seconds."""
    while True:
        await asyncio.sleep(5.0)
        if not manager.active_connections:
            continue

        updated = {}
        for vessel_class in ["CAPESIZE", "PANAMAX", "SUPRAMAX", "HANDYSIZE", "BDI", "BUNKER_VLSFO"]:
            old_val = MARKET_RATES[vessel_class]["rate"]
            # Random micro-fluctuation (-1.5% to +1.5%)
            pct_change = random.uniform(-0.012, 0.014)
            new_val = max(100, int(round(old_val * (1 + pct_change))))
            delta = new_val - old_val
            
            MARKET_RATES[vessel_class]["rate"] = new_val
            MARKET_RATES[vessel_class]["delta"] = delta
            MARKET_RATES[vessel_class]["pctChange"] = round(pct_change * 100, 2)
            updated[vessel_class] = MARKET_RATES[vessel_class]

        await manager.broadcast({
            "type": "RATE_TICK",
            "timestamp": time.time(),
            "rates": updated
        })

async def stream_risk_alerts():
    """Broadcast high-priority risk alerts every 25 seconds."""
    while True:
        await asyncio.sleep(25.0)
        if not manager.active_connections:
            continue

        alert = random.choice(RISK_TEMPLATES).copy()
        alert["id"] = f"ALT-{int(time.time())}"
        alert["timestamp"] = time.strftime("%H:%M:%S UTC", time.gmtime())

        await manager.broadcast({
            "type": "RISK_ALERT",
            "alert": alert
        })

# ── Lifespan Startup Tasks ────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    logger.info("Starting background WebSocket streaming tasks...")
    asyncio.create_task(stream_telematics())
    asyncio.create_task(stream_market_rates())
    asyncio.create_task(stream_risk_alerts())
    logger.info("FreightForecast Pro WebSocket Server ready on port 8765")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="info")
