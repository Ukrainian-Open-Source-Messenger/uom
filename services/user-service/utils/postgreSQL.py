from psycopg2 import pool
from fastapi import HTTPException

DB_URL = "postgresql://postgres:fjQSROBNgYrWwkrUMtKQpGSDNxyDerHl@maglev.proxy.rlwy.net:31076/railway"

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DB_URL
)

def get_connection():
    try:
        return connection_pool.getconn()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB connection error: {str(e)}")

def release_connection(conn):
    connection_pool.putconn(conn)
