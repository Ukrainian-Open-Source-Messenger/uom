import time
import uuid
from fastapi import HTTPException
from models.auth import RegisterRequest, LoginRequest, VerifyRequest, User
from storage import users
from utils.auth import hash_password, verify_password, create_token
from config import JWT_SECRET, JWT_ALGORITHM
from jose import jwt, JWTError

class AuthHandler:

    @staticmethod
    def handle_register(data: RegisterRequest):
        username = data.username.strip()
        password = data.password

        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password required")
        if len(username) < 3:
            raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        if any(u.username == username for u in users.values()):
            raise HTTPException(status_code=409, detail="Username already exists")

        user = User(
            id=f"user_{int(time.time())}_{uuid.uuid4().hex[:8]}",
            username=username,
            password=hash_password(password),
            createdAt=int(time.time() * 1000)
        )

        users[user.id] = user
        token = create_token(user.id, user.username)

        return {
            "success": True,
            "token": token,
            "user": {"id": user.id, "username": user.username}
        }

    @staticmethod
    def handle_login(data: LoginRequest):
        user = next((u for u in users.values() if u.username == data.username), None)
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_token(user.id, user.username)
        return {"success": True, "token": token, "user": {"id": user.id, "username": user.username}}

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
        db_user = users.get(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": db_user.id, "username": db_user.username, "createdAt": db_user.createdAt}
