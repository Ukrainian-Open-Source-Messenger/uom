from fastapi import APIRouter
from models.auth import RegisterRequest, LoginRequest, VerifyRequest
from handlers.auth import AuthHandler

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(data: RegisterRequest):
    return AuthHandler.register(data)

@router.post("/login")
def login(data: LoginRequest):
    return AuthHandler.login(data)

@router.post("/verify")
def verify_token(data: VerifyRequest):
    return AuthHandler.verify_token(data)
