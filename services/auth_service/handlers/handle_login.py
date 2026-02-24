import httpx
import orjson
from fastapi import HTTPException
from schemas.auth import LoginRequest
from utils.auth import verify_password, create_token
from config import USER_SERVICE


async def handle_login(data: LoginRequest):
    email = data.email
    password = data.password

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{USER_SERVICE}/api/get_me_by_email", json={"email": email}, timeout=10
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"User service error: {e.response.text}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to user service: {str(e)}"
        )

    response_server = orjson.loads(response.content)
    user_id = response_server.get("id")
    password_from_service = response_server.get("password")
    username_from_service = response_server.get("username")

    if not verify_password(password, password_from_service):
        raise HTTPException(status_code=400, detail="error")

    token = create_token(user_id=user_id, username=username_from_service)
    return {
        "success": True,
        "token": token,
        "user": {"id": user_id, "username": username_from_service},
    }
