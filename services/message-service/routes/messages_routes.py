import time
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from models import Message, MessageCreate
from storage import messages
from auth import authenticate
from config import MAX_MESSAGES
from typing import List

router = APIRouter()

@router.get("/messages")
def get_messages(limit: int = Query(50), offset: int = Query(0)):
    sliced = messages[-(limit + offset):]
    paginated = sliced[-limit:]
    return {
        "messages": paginated,
        "total": len(messages),
        "limit": limit,
        "offset": offset
    }

@router.get("/messages/recent")
def get_recent_messages(limit: int = Query(50)):
    return {"messages": messages[-limit:], "total": len(messages)}

@router.post("/messages", status_code=201)
def create_message(data: MessageCreate, user=Depends(authenticate)):
    text = data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message text is required")
    if len(text) > 5000:
        raise HTTPException(status_code=400, detail="Message is too long (max 5000 characters)")

    message = Message(
        id=f"msg_{int(time.time())}_{uuid.uuid4().hex[:8]}",
        userId=user["userId"],
        username=user["username"],
        text=text,
        timestamp=int(time.time() * 1000)
    )

    messages.append(message)
    if len(messages) > MAX_MESSAGES:
        messages.pop(0)

    return {"success": True, "message": message}

@router.put("/messages/{message_id}")
def edit_message(message_id: str, data: MessageCreate, user=Depends(authenticate)):
    for msg in messages:
        if msg.id == message_id:
            if msg.userId != user["userId"]:
                raise HTTPException(status_code=403, detail="You can only edit your own messages")

            text = data.text.strip()
            if not text:
                raise HTTPException(status_code=400, detail="Message text is required")

            msg.text = text
            msg.edited = True
            msg.editedAt = int(time.time() * 1000)
            return {"success": True, "message": msg}

    raise HTTPException(status_code=404, detail="Message not found")

@router.delete("/messages/{message_id}")
def delete_message(message_id: str, user=Depends(authenticate)):
    for i, msg in enumerate(messages):
        if msg.id == message_id:
            if msg.userId != user["userId"]:
                raise HTTPException(status_code=403, detail="You can only delete your own messages")

            messages.pop(i)
            return {"success": True, "deletedId": message_id}

    raise HTTPException(status_code=404, detail="Message not found")

@router.get("/messages/search")
def search_messages(query: str = Query(...), limit: int = Query(20)):
    q = query.strip().lower()
    if not q:
        raise HTTPException(status_code=400, detail="Search query is required")

    result = [m for m in messages if q in m.text.lower()][-limit:]
    return {"messages": result, "query": query, "total": len(result)}

@router.get("/messages/stats")
def messages_stats():
    user_stats = {}
    for msg in messages:
        user_stats[msg.username] = user_stats.get(msg.username, 0) + 1

    return {
        "totalMessages": len(messages),
        "userStats": user_stats,
        "oldestMessage": messages[0].timestamp if messages else None,
        "newestMessage": messages[-1].timestamp if messages else None
    }
