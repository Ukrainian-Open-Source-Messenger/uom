import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = str(os.getenv("JWT_SECRET", "your-secret-key-change-in-production"))
JWT_ALGORITHM = str(os.getenv("JWT_ALGORITHM", "HS256"))

USER_SERVICE = str(os.getenv("USER_SERVICE", "http://localhost:3004"))
