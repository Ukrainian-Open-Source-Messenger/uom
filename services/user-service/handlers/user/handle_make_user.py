import time
import uuid_utils as uuid
from fastapi import HTTPException
from models.user import MakeRequest
from utils.postgreSQL import get_connection, release_connection

async def handle_make_user(data: MakeRequest):
    username = data.username.strip()
    password = data.password
    email = data.email
    createdat = int(time.time() * 1000)

    if not username or not password or not email:
        raise HTTPException(status_code=400, detail="Username, password and email required")
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user_id = uuid.uuid7().bytes

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (id, username, password, createdat, email)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, username, password, createdat, email))
            conn.commit()

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    finally:
        release_connection(conn)

    return {
        "id": user_id,
        "username": username,
        "email": email,
        "createdat": createdat
    }