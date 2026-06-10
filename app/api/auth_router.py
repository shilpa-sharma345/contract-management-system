from fastapi import APIRouter, Depends
from typing import List
from app.model.models import ContractResponse, ContractListResponse
from app.utils.dependencies import admin_required
from app.auth.auth_functions import (
    register,
    login,
    get_me,
    get_contracts,
    upload_test,
    create_contract,
    delete_contract,
    get_dashboard,
    get_filtered_contracts,
    get_contract_by_id,
    upload_contract,
    test_expiry_reminder
)

# -------------------------
# AUTHENTICATION ROUTER
# -------------------------
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_router.post("/register")(register)
auth_router.post("/login")(login)
auth_router.get("/me")(get_me)

# -------------------------
# CONTRACTS ROUTER
# -------------------------
contracts_router = APIRouter(prefix="/contracts", tags=["Contracts"])

contracts_router.get("", response_model=List[ContractListResponse])(get_contracts)
contracts_router.post("/create/contract")(create_contract)
contracts_router.delete("/delete/{contract_id}", dependencies=[Depends(admin_required)])(delete_contract)
contracts_router.get("/search", response_model=List[ContractListResponse])(get_filtered_contracts)
contracts_router.post("/upload", response_model=ContractResponse)(upload_contract)
contracts_router.get("/{contract_id}", response_model=ContractResponse)(get_contract_by_id)

# -------------------------
# DASHBOARD ROUTER
# -------------------------
dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

dashboard_router.get("")(get_dashboard)

# -------------------------
# UPLOAD TEST ROUTER
# -------------------------
upload_router = APIRouter(prefix="/upload", tags=["Upload"])

upload_router.post("")(upload_test)

# -------------------------
# REMINDERS ROUTER
# -------------------------
reminders_router = APIRouter(prefix="/reminders", tags=["Reminders"])

reminders_router.post("/send")(test_expiry_reminder)