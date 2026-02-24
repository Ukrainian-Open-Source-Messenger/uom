import httpx
import orjson
from fastapi import HTTPException
from schemas.auth import RegisterRequest
from utils.auth import hash_password, create_token
from config import USER_SERVICE


async def handle_register(data: RegisterRequest):
    password = data.password
    email = data.email
    username = data.username.strip()

    payload = {
        "password": hash_password(password),
        "email": email,
        "username": username,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{USER_SERVICE}/api/make_user", json=payload, timeout=10
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

    token = create_token(user_id=user_id, username=username)

    return {
        "success": True,
        "token": token,
        "user": {
            "id": user_id,
            "username": username,
        },
    }
