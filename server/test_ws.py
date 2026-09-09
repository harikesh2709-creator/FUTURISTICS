"""
Test client to verify FreightForecast Pro WebSocket Server
"""
import asyncio
import json
import websockets

async def test_connection():
    uri = "ws://127.0.0.1:8765/ws"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Waiting for INITIAL_STATE...")
            msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(msg)
            print(f"Received packet type: {data.get('type')}")
            assert data.get('type') == 'INITIAL_STATE', "Expected INITIAL_STATE"
            assert "fleet" in data, "Expected fleet in initial state"
            assert len(data["fleet"]) > 0, "Expected non-empty fleet"
            print(f"Fleet count: {len(data['fleet'])} vessels")

            # Test ping/pong
            print("Sending ping...")
            await websocket.send(json.dumps({"type": "ping", "t": 123456789}))
            pong_msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            pong_data = json.loads(pong_msg)
            print(f"Received pong packet: {pong_data}")
            assert pong_data.get("type") == "pong", "Expected pong response"
            print("WebSocket test passed successfully!")
            return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
