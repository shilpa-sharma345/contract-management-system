from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from uuid import UUID


class UserRole(str, Enum):
    admin = "admin"
    contract_manager = "contract_manager"
    department_user = "department_user"
    viewer = "viewer"


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
    GEMINI_API_KEY: str

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
    id: UUID
    full_name: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


# ── Screen 3: contract listing (no AI fields) ──────────────────
class ContractListResponse(BaseModel):
    id: UUID
    title: str
    department: str | None = None
    start_date: datetime | None = None
    expiry_date: datetime | None = None
    status: str

    class Config:
        from_attributes = True


# ── Screen 3 → View: full detail including AI fields ──────────
class ContractResponse(BaseModel):
    id: UUID
    title: str
    status: str
    department: str | None = None

    # File
    file_path: str | None = None

    # Contract dates
    start_date: datetime | None = None
    expiry_date: datetime | None = None

    # Contract details
    supplier: str | None = None
    value: str | None = None
    notice_period: str | None = None

    # AI results
    ai_summary: str | None = None
    risk_flag: str | None = None
    key_clauses: str | None = None

    uploaded_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ContractCreate(BaseModel):
    title: str
    status: str = "active"
    department: str | None = None
    start_date: datetime | None = None
    expiry_date: datetime | None = None