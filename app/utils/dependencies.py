from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError

from app.db.db import AsyncSessionLocal
from app.db.models import User
from sqlalchemy import select

from app.constants.environ import SECRET_KEY, ALGORITHM
from app.model.models import UserRole

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired"
        )

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user


def require_role(*allowed_roles: UserRole):
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role not in [r.value for r in allowed_roles]:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this resource"
            )
        return current_user
    return role_checker