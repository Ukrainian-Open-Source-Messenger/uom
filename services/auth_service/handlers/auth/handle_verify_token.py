from models.auth import VerifyRequest
from config import JWT_SECRET, JWT_ALGORITHM
from jose import jwt, JWTError

def handle_verify_token(data: VerifyRequest):
    try:
        decoded = jwt.decode(data.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"valid": True, "user": {"id": decoded["userId"], "username": decoded["username"]}}
    except JWTError:
        return {"valid": False, "error": "Invalid token"}