from sqlalchemy import Boolean, Column, Integer, String , DateTime , ForeignKey
from sqlalchemy.sql import func

from app.db.db import Base

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)

    def soft_delete(self):
        self.is_deleted = True
        
class User(Base,SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False, default="department_user")

class Contract(Base,SoftDeleteMixin):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="active")
    department = Column(String(100), nullable=True)

    # File
    file_path = Column(String(500), nullable=True)

    # Contract dates
    start_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)

    # Contract details (extracted by AI)
    supplier = Column(String(255), nullable=True)
    value = Column(String(100), nullable=True)
    notice_period = Column(String(100), nullable=True)

    # AI results
    ai_summary = Column(String, nullable=True)
    risk_flag = Column(String, nullable=True)
    key_clauses = Column(String, nullable=True)

    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)