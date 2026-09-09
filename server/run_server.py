"""
Runner script for FreightForecast Pro Full-Stack Application.
Serves Dashboard UI & Real-Time WebSocket on 127.0.0.1:8765.
"""

import sys
import os
import webbrowser
import threading
import time

try:
    import uvicorn
except ImportError:
    print("[ERROR] uvicorn is not installed. Please run: pip install -r server/requirements.txt")
    sys.exit(1)

def open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:8765/")
    except Exception as e:
        print(f"[INFO] Open browser manually at http://127.0.0.1:8765/ ({e})")

if __name__ == "__main__":
    # Ensure UTF-8 output if possible
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    print("=" * 65)
    print("  [+] FreightForecast Pro - Intelligent Freight Forecasting")
    print("  --> Web Dashboard:  http://127.0.0.1:8765/")
    print("  --> WebSocket API:  ws://127.0.0.1:8765/ws")
    print("  --> Health Check:   http://127.0.0.1:8765/health")
    print("=" * 65)
    
    # Launch browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run("ws_server:app", host="127.0.0.1", port=8765, reload=False, app_dir=os.path.dirname(__file__))
