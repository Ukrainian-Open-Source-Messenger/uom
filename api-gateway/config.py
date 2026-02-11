import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8080))

AUTH_SERVICE = os.getenv("AUTH_SERVICE", "http://localhost:3001")
MESSAGE_SERVICE = os.getenv("MESSAGE_SERVICE", "http://localhost:3002")
REALTIME_SERVICE = os.getenv("REALTIME_SERVICE", "ws://localhost:3003")
