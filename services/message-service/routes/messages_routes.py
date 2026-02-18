from fastapi import APIRouter, Depends, Query
from models.message import MessageCreate
from utils.auth import authenticate
from handlers.messages import Messages

router = APIRouter()


@router.get("/messages")
async def get_messages(limit: int = Query(50), offset: int = Query(0)):
    return await Messages.handle_get_messages(limit, offset)


@router.get("/messages/recent")
async def get_recent_messages(limit: int = Query(50)):
    return await Messages.handle_get_recent_messages(limit)


@router.post("/messages", status_code=201)
async def create_message(data: MessageCreate, user=Depends(authenticate)):
    return await Messages.handle_create_message(data, user)
