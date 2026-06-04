import re
from typing import Optional,List
from pydantic_settings import BaseSettings
from pydantic import BaseModel,Field, EmailStr,  field_validator,model_validator
from datetime import datetime
from enum import Enum
from uuid import UUID

class UserRole(str, Enum):
    admin = "admin"
    contract_manager = "contract_manager"
    department_user = "department_user"


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
    role: UserRole = UserRole.department_user


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True

class ContractResponse(BaseModel):
    id: int
    title: str
    status: str
    expiry_date: datetime | None
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class ContractCreate(BaseModel):
    title: str
    status: str = "active"
    expiry_date: datetime | None = None