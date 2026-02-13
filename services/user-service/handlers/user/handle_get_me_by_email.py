from fastapi import HTTPException
from models.user import GetMeByEmailRequest
from utils.postgreSQL import get_connection, release_connection

def handle_get_me_by_email(data: GetMeByEmailRequest):
    email = data.email.strip() if data.email else None

    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email, createdat, password
                FROM users
                WHERE email = %s
                LIMIT 1
            """, (email,))
            user = cur.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")


            user_data = {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "createdat": user[3],
                "password": user[4]
            }

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    finally:
        release_connection(conn)

    return user_data


