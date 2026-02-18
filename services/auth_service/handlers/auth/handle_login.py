import httpx
import orjson
from fastapi import HTTPException
from services.auth_service.models.auth import LoginRequest
from utils.auth import verify_password, create_token
from fastapi import HTTPException
from config import USER_SERVICE

async def handle_login(data: LoginRequest):
    email = data.email
    username = data.username.strip()
    password = data.password

    try: 
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{USER_SERVICE}/api/get_me_by_email", json={"email": email}, timeout=10)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"User service error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to user service: {str(e)}"
        )

    response_server = orjson.loads(response.content)
    user_id = response_server.get("id")
    password_from_service = response_server.get("password")
    username_from_service = response_server.get("username")

    if username != username_from_service or verify_password(password, password_from_service) != True:
        raise HTTPException(status_code=400, detail="error")
    
    token = create_token(user_id, username_from_service)
    return {"success": True, "token": token, "user": {"id": user_id, "username": username_from_service}}