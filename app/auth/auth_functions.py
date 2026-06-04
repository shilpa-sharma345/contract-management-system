from fastapi import Depends
from fastapi import HTTPException
from app.db.db import create_connection, close_connection
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.contract_service import ContractService
from app.model.models import UserRole, ContractResponse
from typing import List
from app.model.models import ContractCreate
from app.services.contract_service import ContractService


from app.model.models import (
    UserCreate,
    UserLogin,
    UserResponse
)
from app.auth.auth_service import AuthService

#  dependency import
from app.utils.dependencies import get_current_user, require_role




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

async def delete_contract(
    contract_id: int,
    current_user=Depends(
        require_role(UserRole.admin)
    )
):
    try:
        contract = await ContractService.delete_contract(contract_id)

        if not contract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )

        return {
            "message": "Contract deleted successfully",
            "id": contract_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

async def get_contracts(
    current_user=Depends(require_role(
        UserRole.admin,
        UserRole.contract_manager,
        UserRole.department_user
    ))
):
    try:
        return await ContractService.get_all_contracts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# ADMIN ONLY TEST
# -------------------------
async def admin_test(
    current_user=Depends(
        require_role(UserRole.admin)
    )
):
    return {
        "message": "Admin Access Granted",
        "user": current_user.email,
        "role": current_user.role
    }


# -------------------------
# ADMIN + CONTRACT MANAGER TEST
# -------------------------
async def upload_test(
    current_user=Depends(
        require_role(
            UserRole.admin,
            UserRole.contract_manager
        )
    )
):
    return {
        "message": "Upload Access Granted",
        "user": current_user.email,
        "role": current_user.role
    }

async def create_contract(
    contract: ContractCreate,
    current_user=Depends(
        require_role(
            UserRole.admin,
            UserRole.contract_manager
        )
    )
):
    try:
        return await ContractService.create_contract(
            contract,
            current_user.id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )