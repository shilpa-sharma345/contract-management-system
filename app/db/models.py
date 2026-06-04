from sqlalchemy import Column, Integer, String , DateTime , ForeignKey
from sqlalchemy.sql import func

from app.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False, default="department_user")


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    status = Column(String(50), nullable=False, default="active")

    expiry_date = Column(DateTime, nullable=True)

    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)