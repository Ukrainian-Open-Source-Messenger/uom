from fastapi import APIRouter
from schemas.auth import RegisterRequest, LoginRequest
from handlers import AuthHandler

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(data: RegisterRequest):
    return await AuthHandler.register(data)


@router.post("/login")
async def login(data: LoginRequest):
    return await AuthHandler.login(data)
