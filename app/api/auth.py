from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.schemas.auth_schema import (
    UserCreate,
    UserLogin,
    UserResponse
)
from app.services.auth_service import AuthService

#  dependency import
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# -------------------------
# REGISTER API
# -------------------------
@router.post(
    "/register",
    response_model=UserResponse
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await AuthService.register_user(user, db)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# -------------------------
# LOGIN API
# -------------------------
@router.post("/login")
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await AuthService.login_user(user, db)

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


# -------------------------
# PROTECTED ROUTE
# -------------------------
@router.get("/me")
async def get_me(
    current_user = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role
    }