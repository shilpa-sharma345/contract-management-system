from fastapi import Depends
from fastapi import HTTPException
from app.db.db import create_connection, close_connection
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import (
    UserCreate,
    UserLogin,
    UserResponse
)
from app.auth.auth_service import AuthService

#  dependency import
from app.utils.dependencies import get_current_user





async def register( user: UserCreate):
    try:
        return await AuthService.register_user(user)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
async def login( user: UserLogin,):
    try:
        return await AuthService.login_user(user)

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

async def get_me(
    current_user = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role
    }    
