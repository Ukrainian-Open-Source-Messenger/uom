from fastapi import FastAPI
from middleware import add_middlewares
from routes import router
from config import PORT
import uvicorn

app = FastAPI()
add_middlewares(app)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
