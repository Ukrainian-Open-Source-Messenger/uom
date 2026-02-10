from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.messages_routes import router as messages_router

app = FastAPI(title="message-service")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(messages_router)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 3002))
    uvicorn.run(app, host="0.0.0.0", port=port)
