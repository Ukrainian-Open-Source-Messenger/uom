from fastapi import APIRouter
from models.user import MakeRequest, GetMeByEmailRequest, GetMeByIdRequest
from handlers.user import UserHandler

router = APIRouter(prefix="/api")

@router.post("/make_user")
def register(data: MakeRequest):
    return UserHandler.make_user(data)

@router.post("/get_me_by_email")
def me(data: GetMeByEmailRequest):
    return UserHandler.get_me_by_email(data)

@router.post("/get_me_by_id")
def me(data: GetMeByIdRequest):
    return UserHandler.get_me_by_id(data)
