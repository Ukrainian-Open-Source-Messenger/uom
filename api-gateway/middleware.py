import time
from datetime import datetime
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

def add_middlewares(app):
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Logging
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = int((time.time() - start) * 1000)
        print(
            f"[{datetime.utcnow().isoformat()}] "
            f"{request.method} {request.url.path} - {duration}ms"
        )
        return response
