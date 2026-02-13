from fastapi import APIRouter, Depends
from models.auth import RegisterRequest, LoginRequest, VerifyRequest
from handlers.auth_handler import AuthHandler
from utils.auth import authenticate

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(data: RegisterRequest):
    return AuthHandler.handle_register(data)

@router.post("/login")
def login(data: LoginRequest):
    return AuthHandler.handle_login(data)

@router.post("/verify")
def verify_token(data: VerifyRequest):
    return AuthHandler.handle_verify_token(data)

@router.get("/me")
def me(user=Depends(authenticate)):
    return AuthHandler.handle_me(user)
