import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_TEST = True
DB_TEST_URL = os.getenv("DB_TEST_URL")

# AUTH_SERVICE = os.getenv("AUTH_SERVICE", "http://localhost:3001")
