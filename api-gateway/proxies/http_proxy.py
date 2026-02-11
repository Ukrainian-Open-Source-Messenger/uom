import httpx
from fastapi import Request
from fastapi.responses import JSONResponse
from config import AUTH_SERVICE, MESSAGE_SERVICE

async def proxy_request(request: Request, target_base: str, rewrite_from: str, rewrite_to: str):
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

# HTTP proxy functions
async def auth_proxy(request: Request, path: str):
    return await proxy_request(request, AUTH_SERVICE, "/api/auth", "/auth")

async def messages_proxy(request: Request, path: str):
    return await proxy_request(request, MESSAGE_SERVICE, "/api/messages", "/messages")
