from fastapi import HTTPException
from models.user import GetMeByIdRequest
from utils.postgreSQL import get_connection, release_connection

async def handle_get_me_by_id(data: GetMeByIdRequest):
    id = data.id.strip() if data.id else None

    if not id:
        raise HTTPException(status_code=400, detail="Email is required")

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT username, createdat
                FROM users
                WHERE email = %s
                LIMIT 1
            """, (id,))
            user = cur.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")


            user_data = {
                "id": id,
                "username": user[0],
                "createdat": user[2],
            }

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    finally:
        release_connection(conn)

    return user_data