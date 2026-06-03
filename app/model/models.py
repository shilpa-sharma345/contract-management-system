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
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    RESET_TOKEN_EXPIRE_MINUTES: int



    class Config:
        env_file = ".env"



class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True