import time
import uuid_utils as uuid
from fastapi import HTTPException
from models.message import Message, MessageCreate
from storage import messages
from config import MAX_MESSAGES

class Messages:

    @staticmethod
    async def handle_get_messages(limit: int = 50, offset: int = 0):
        sliced = messages[-(limit + offset):]
        paginated = sliced[-limit:]
        return {
            "messages": paginated,
            "total": len(messages),
            "limit": limit,
            "offset": offset
        }

    @staticmethod
    async def handle_get_recent_messages(limit: int = 50):
        return {
            "messages": messages[-limit:],
            "total": len(messages)
        }

    @staticmethod
    async def handle_create_message(data: MessageCreate, user):
        text = data.text.strip()

        if not text:
            raise HTTPException(status_code=400, detail="Message text is required")

        if len(text) > 5000:
            raise HTTPException(
                status_code=400,
                detail="Message is too long (max 5000 characters)"
            )

        message = Message(
            id=uuid.uuid7().bytes,
            userId=user["userId"],
            username=user["username"],
            text=text,
            timestamp=int(time.time() * 1000)
        )

        messages.append(message)

        if len(messages) > MAX_MESSAGES:
            messages.pop(0)

        return {"success": True, "message": message}
