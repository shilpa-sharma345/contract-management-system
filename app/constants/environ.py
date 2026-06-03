import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
DB_HOST = os.getenv("DB_HOST")
if not DB_HOST:
    raise RuntimeError("DB_HOST not found")

DB_NAME = os.getenv("DB_NAME")
if not DB_NAME:
    raise RuntimeError("DB_NAME not found")

DB_USER = os.getenv("DB_USER")
if not DB_USER:
    raise RuntimeError("DB_USER not found")

DB_PASSWORD = os.getenv("DB_PASSWORD")
if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD not found")

DB_PORT = os.getenv("DB_PORT")
if not DB_PORT:
    raise RuntimeError("DB_PORT not found")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not found")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", 15))