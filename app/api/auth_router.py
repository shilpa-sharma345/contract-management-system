from fastapi import APIRouter, Depends
from typing import List
from app.model.models import ContractResponse
from app.utils.dependencies import contractor_required
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
    upload_contract
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

contracts_router.get("", response_model=List[ContractResponse])(get_contracts)
contracts_router.post("/create/contract")(create_contract)
contracts_router.delete("/delete/{contract_id}", dependencies=[Depends(contractor_required)])(delete_contract)
contracts_router.get("/search")(get_filtered_contracts)
contracts_router.post("/upload")(upload_contract)
contracts_router.get("/{contract_id}")(get_contract_by_id)

# -------------------------
# DASHBOARD ROUTER
# -------------------------
dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

dashboard_router.get("")(get_dashboard)

# -------------------------
# UPLOAD TEST ROUTER  (can remove later)
# -------------------------
upload_router = APIRouter(prefix="/upload", tags=["Upload"])

upload_router.post("")(upload_test)