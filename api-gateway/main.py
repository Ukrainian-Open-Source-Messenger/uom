import asyncio
import os
import time
from datetime import datetime

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from dotenv import load_dotenv
import httpx
import websockets

load_dotenv()

PORT = int(os.getenv("PORT", 8080))

AUTH_SERVICE = os.getenv("AUTH_SERVICE", "http://localhost:3001")
MESSAGE_SERVICE = os.getenv("MESSAGE_SERVICE", "http://localhost:3002")
REALTIME_SERVICE = os.getenv("REALTIME_SERVICE", "ws://localhost:3003")

app = FastAPI()

# ========= CORS =========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========= Logging middleware =========
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = int((time.time() - start) * 1000)

    print(
        f"[{datetime.utcnow().isoformat()}] "
        f"{request.method} {request.url.path} - {duration}ms"
    )
    return response


# ========= HTTP PROXY =========
async def proxy_request(request: Request, target_base: str, rewrite_from: str, rewrite_to: str):
    url = str(request.url)
    path = request.url.path.replace(rewrite_from, rewrite_to, 1)
    target_url = f"{target_base}{path}"

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=dict(request.headers),
            params=request.query_params,
            content=await request.body(),
        )

    return JSONResponse(
        status_code=response.status_code,
        content=response.json() if response.content else None,
        headers=response.headers,
    )


# Auth
@app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def auth_proxy(request: Request, path: str):
    return await proxy_request(
        request,
        AUTH_SERVICE,
        "/api/auth",
        "/auth",
    )


# Messages
@app.api_route("/api/messages/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def messages_proxy(request: Request, path: str):
    return await proxy_request(
        request,
        MESSAGE_SERVICE,
        "/api/messages",
        "/messages",
    )


@app.get("/")
async def root():
    return PlainTextResponse("API Gateway is running")


# ========= WebSocket Proxy =========
@app.websocket("/ws")
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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )
