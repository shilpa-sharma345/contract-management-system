from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from typing import List
from app.model.models import ContractResponse

from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.auth_functions import (
    register,
    login,
    get_me,
    get_contracts,
    admin_test,
    upload_test,
    create_contract,
    delete_contract
)
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

auth_router.get("/contracts", response_model=List[ContractResponse])(get_contracts)
# RBAC TEST ROUTES

auth_router.get("/admin")(admin_test)

auth_router.post("/upload")(upload_test)

auth_router.post("/contracts")(create_contract)

auth_router.delete("/contracts/{contract_id}")(delete_contract)