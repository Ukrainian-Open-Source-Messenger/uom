from fastapi import HTTPException
from models.auth import RegisterRequest, LoginRequest, VerifyRequest
from utils.auth import hash_password, verify_password, create_token
from config import JWT_SECRET, JWT_ALGORITHM
from jose import jwt, JWTError
import httpx
from fastapi import HTTPException
from config import USER_SERVICE

class AuthHandler:

    @staticmethod
    def handle_register(data: RegisterRequest):
        username = data.username.strip()
        password = data.password
        email = data.email

        if not username or not password or not email:
            raise HTTPException(status_code=400, detail="Username, password and email required")
        if len(username) < 3:
            raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        payload = {
            "username": username,
            "password": hash_password(password),
            "email": email,
        }

        try:
            response = httpx.post(f"{USER_SERVICE}/api/make_user", json=payload, timeout=10)
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

        response_server = response.json()
        user_id = response_server.get("id")
        username_from_service = response_server.get("username")

        token = create_token(user_id, username_from_service)

        return {
            "success": True,
            "token": token,
            "user": {
                "id": user_id,
                "username": username_from_service
            }
        }


    @staticmethod
    def handle_login(data: LoginRequest):
        email = data.email
        username = data.username.strip()
        password = data.password

        try:
            response = httpx.post(f"{USER_SERVICE}/api/get_me_by_email", json={"email": email}, timeout=10)
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

        response_server = response.json()
        user_id = response_server.get("id")
        password_from_service = response_server.get("password")
        username_from_service = response_server.get("username")

        if username != username_from_service or verify_password(password, password_from_service) != True:
            raise HTTPException(status_code=400, detail="error")
        
        token = create_token(user_id, username_from_service)
        return {"success": True, "token": token, "user": {"id": user_id, "username": username_from_service}}

    @staticmethod
    def handle_verify_token(data: VerifyRequest):
        try:
            decoded = jwt.decode(data.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return {"valid": True, "user": {"id": decoded["userId"], "username": decoded["username"]}}
        except JWTError:
            return {"valid": False, "error": "Invalid token"}

    @staticmethod
    def handle_me(user):
        user_id = user["userId"]

        try:
            response = httpx.post(f"{USER_SERVICE}/api/get_me_by_email", json={"user_id": user_id}, timeout=10)
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

        response_server = response.json()
        user_id = response_server.get("id")
        createdat_from_service = response_server.get("createdat")
        username_from_service = response_server.get("username")

        return {"id": user_id, "username": username_from_service, "createdAt": createdat_from_service}
