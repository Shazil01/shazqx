from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from strategies import analyze_market
from quotex_api import QuotexClient
import json
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# WebSocket connections
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            command = json.loads(data)
            
            if command.get('action') == 'start_bot':
                # Start trading loop
                asyncio.create_task(trading_loop(websocket))
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)

async def trading_loop(websocket):
    client = QuotexClient()
    while True:
        try:
            signals = analyze_market(client)
            if signals:
                await websocket.send_json({
                    "type": "signal",
                    **signals
                })
        except Exception as e:
            print(f"Trading error: {e}")
        await asyncio.sleep(5)  # Check every 5 seconds