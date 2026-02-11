from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from proxies.http_proxy import auth_proxy, messages_proxy
from proxies.ws_proxy import websocket_proxy

router = APIRouter()

# HTTP routes
router.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])(auth_proxy)
router.api_route("/api/messages/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])(messages_proxy)
router.get("/")(lambda: PlainTextResponse("API Gateway is running"))

# WS route
router.websocket("/ws")(websocket_proxy)
