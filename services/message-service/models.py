from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    id: str
    userId: str
    username: str
    text: str
    timestamp: int
    edited: Optional[bool] = False
    editedAt: Optional[int] = None

class MessageCreate(BaseModel):
    text: str
