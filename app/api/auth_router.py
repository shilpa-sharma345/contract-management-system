from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.auth_functions import register,login,get_me
from app.db.dependencies import get_db
from app.model.models import (
    UserCreate,
    UserLogin,
    UserResponse
)
from app.auth.auth_service import AuthService

#  dependency import
from app.utils.dependencies import get_current_user


auth_router = APIRouter(prefix="/auth",tags=["Authentication"])


auth_router.post("/register")(register)
auth_router.post("/login")(login)
auth_router.get("/me")(get_me)
