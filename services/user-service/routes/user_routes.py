from fastapi import APIRouter
from models.user import MakeRequest, GetMeByEmailRequest, GetMeByIdRequest
from handlers.user import UserHandler

router = APIRouter(prefix="/api")

@router.post("/make_user")
async def register(data: MakeRequest):
    return await UserHandler.make_user(data)

@router.post("/get_me_by_email")
async def me(data: GetMeByEmailRequest):
    return await UserHandler.get_me_by_email(data)

@router.post("/get_me_by_id")
async def me(data: GetMeByIdRequest):
    return await UserHandler.get_me_by_id(data)
