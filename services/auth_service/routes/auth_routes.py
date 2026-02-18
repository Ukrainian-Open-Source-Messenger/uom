from fastapi import APIRouter
from models.auth import RegisterRequest, LoginRequest, VerifyRequest
from handlers.auth import AuthHandler

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(data: RegisterRequest):
    return await AuthHandler.register(data)

@router.post("/login")
async def login(data: LoginRequest):
    return await AuthHandler.login(data)

@router.post("/verify")
async def verify_token(data: VerifyRequest):
    return await AuthHandler.verify_token(data)
