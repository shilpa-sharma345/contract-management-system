from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import create_connection, close_connection 
from app.db.models import User
from app.model.models import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token


class AuthService:

    # -------------------------
    # REGISTER USER
    # -------------------------
    @staticmethod
    async def register_user(
        user_data: UserCreate,
    ):
        session = await create_connection()
        try:
            result = await session.execute(
                select(User).where(User.email == user_data.email)
            )

            existing_user = result.scalar_one_or_none()

            if existing_user:
                raise ValueError("Email already registered")

            # create new user
            new_user = User(
                full_name=user_data.full_name,
                email=user_data.email,
                hashed_password=hash_password(user_data.password),
                role=user_data.role.value
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            return new_user
        finally:
            await close_connection(session)
    # -------------------------
    # LOGIN USER
    # -------------------------
    @staticmethod
    async def login_user(user_data: UserLogin,):
        session = await create_connection()
        try:
            result = await session.execute(
                select(User).where(User.email == user_data.email)
            )

            user = result.scalar_one_or_none()

            if not user:
                raise ValueError("Invalid credentials")

            if not verify_password(
                user_data.password,
                user.hashed_password
            ):
                raise ValueError("Invalid credentials")

            token = create_access_token(
                data={
                    "user_id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            )

            return {
                "access_token": token,
                "token_type": "bearer"
            }
        finally:
            await close_connection(session)

