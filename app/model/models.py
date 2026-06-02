import re
from typing import Optional,List
from pydantic_settings import BaseSettings
from pydantic import BaseModel,Field, EmailStr,  field_validator,model_validator
from datetime import datetime, time, date
from enum import Enum
from uuid import UUID


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int


    class Config:
        env_file = ".env"