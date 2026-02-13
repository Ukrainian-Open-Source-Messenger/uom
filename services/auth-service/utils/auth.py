import time
from jose import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from config import JWT_SECRET, JWT_ALGORITHM

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False

def create_token(user_id: str, username: str) -> str:
    payload = {
        "userId": user_id,
        "username": username,
        "iat": int(time.time())
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
