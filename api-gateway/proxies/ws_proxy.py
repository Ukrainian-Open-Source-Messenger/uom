import asyncio
import websockets
from fastapi import WebSocket, WebSocketDisconnect
from config import REALTIME_SERVICE

async def websocket_proxy(client_ws: WebSocket):
    await client_ws.accept()
    print("WS connected")

    try:
        async with websockets.connect(REALTIME_SERVICE) as backend_ws:

            async def client_to_backend():
                while True:
                    data = await client_ws.receive_text()
                    await backend_ws.send(data)

            async def backend_to_client():
                while True:
                    data = await backend_ws.recv()
                    await client_ws.send_text(data)

            await asyncio.gather(client_to_backend(), backend_to_client())

    except WebSocketDisconnect:
        print("WS disconnected")
