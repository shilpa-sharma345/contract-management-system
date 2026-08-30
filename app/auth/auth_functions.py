from fastapi import Depends, HTTPException, UploadFile, File, Form
from app.db.db import create_connection, close_connection
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.contract_service import ContractService
from app.model.models import UserRole, ContractResponse
from typing import List
from app.services.reminder_service import ReminderService
from app.model.models import ContractCreate
from app.model.models import (
    UserCreate,
    UserLogin,
    UserResponse
)
from app.auth.auth_service import AuthService
from app.utils.dependencies import get_current_user, require_role
from uuid import UUID


async def register(user: UserCreate):
    try:
        return await AuthService.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def login(user: UserLogin):
    try:
        return await AuthService.login_user(user)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


async def get_me(
    current_user=Depends(get_current_user)
):
    return {
        "id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role
    }


async def delete_contract(
    contract_id: UUID,
    current_user=Depends(require_role(UserRole.admin))
):
    try:
        contract = await ContractService.delete_contract(contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        return {
            "message": "Contract deleted successfully",
            "id": str(contract_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_contracts(
    current_user=Depends(require_role(
        UserRole.admin,
        UserRole.contract_manager,
        UserRole.department_user,
        UserRole.viewer
    ))
):
    try:
        return await ContractService.get_all_contracts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def upload_test(
    current_user=Depends(require_role(
        UserRole.admin,
        UserRole.contract_manager
    ))
):
    return {
        "message": "Upload Access Granted",
        "user": current_user.email,
        "role": current_user.role
    }


async def create_contract(
    contract: ContractCreate,
    current_user=Depends(require_role(
        UserRole.admin,
        UserRole.contract_manager
    ))
):
    try:
        return await ContractService.create_contract(
            contract,
            current_user.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# DASHBOARD
# -------------------------
async def get_dashboard(
    current_user=Depends(require_role(
        UserRole.admin,
        UserRole.contract_manager,
        UserRole.department_user,
        UserRole.viewer
    ))
):
    try:
        total_active = await ContractService.get_total_active_contracts()
        expiring_this_month = await ContractService.get_expiring_this_month()
        expiring_next_quarter = await ContractService.get_expiring_next_quarter()
        upcoming_expirations = await ContractService.get_upcoming_expirations()

        return {
            "total_active_contracts": total_active,
            "expiring_this_month": len(expiring_this_month),
            "expiring_next_quarter": len(expiring_next_quarter),
            "upcoming_expirations": upcoming_expirations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# GET CONTRACTS WITH FILTERS
# -------------------------
async def get_filtered_contracts(
    search: str | None = None,
    department: str | None = None,
    status: str | None = None,
    current_user=Depends(require_role(
        UserRole.admin,
        UserRole.contract_manager,
        UserRole.department_user,
        UserRole.viewer
    ))
):
    try:
        return await ContractService.get_filtered_contracts(
            search=search,
            department=department,
            status=status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# GET SINGLE CONTRACT BY ID
# -------------------------
async def get_contract_by_id(
    contract_id: UUID,
    current_user=Depends(require_role(
        UserRole.admin,
        UserRole.contract_manager,
        UserRole.department_user,
        UserRole.viewer
    ))
):
    try:
        contract = await ContractService.get_contract_by_id(contract_id)
        if not contract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )
        return contract
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# UPLOAD CONTRACT WITH AI
# -------------------------
async def upload_contract(
    title: str = Form(...),
    department: str = Form(...),
    file: UploadFile = File(...),
    current_user=Depends(require_role(
        UserRole.admin,
        UserRole.contract_manager
    ))
):
    try:
        return await ContractService.upload_contract(
            title=title,
            department=department,
            user_id=current_user.id,
            file=file
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# MANUAL TRIGGER — SEND EXPIRY REMINDERS
# -------------------------
async def test_expiry_reminder(
    current_user=Depends(require_role(UserRole.admin))
):
    try:
        for days in [30, 7, 1]:
            await ReminderService.send_expiry_reminders(days)
        return {"message": "Expiry reminders processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))