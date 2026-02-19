from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.messages_routes import router as messages_router
from fastapi.responses import ORJSONResponse

app = FastAPI(title="message-service", response_class=ORJSONResponse)

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
