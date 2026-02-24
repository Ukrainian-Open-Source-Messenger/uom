import time
from jose import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from config import JWT_SECRET, JWT_ALGORITHM
import uuid_utils as uuid

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False


def create_token(user_id: str, username: str, is_refresh: bool = False) -> str:
    payload = {
        "userId": user_id,
        "username": username,
        "iat": int(time.time()),
        "type": "refresh" if is_refresh else "access",
        "jti": uuid.uuid7().hex if is_refresh else None,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
