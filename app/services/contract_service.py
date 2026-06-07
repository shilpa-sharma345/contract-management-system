from sqlalchemy import select, delete, func
from app.db.db import create_connection, close_connection
from app.db.models import Contract
from app.model.models import ContractCreate
from datetime import datetime, timedelta
from app.services.ai_service import analyze_contract
from app.utils.file_handler import save_upload_file, extract_text_from_file
from fastapi import UploadFile

class ContractService:

    # -------------------------
    # GET ALL CONTRACTS
    # -------------------------
    @staticmethod
    async def get_all_contracts():
        session = await create_connection()
        try:
            result = await session.execute(
                select(Contract).where(Contract.is_deleted == False)
            )
            contracts = result.scalars().all()
            return contracts
        finally:
            await close_connection(session)

    # -------------------------
    # CREATE CONTRACT
    # -------------------------
    @staticmethod
    async def create_contract(contract_data: ContractCreate, user_id: int):
        session = await create_connection()
        try:
            expiry_date = contract_data.expiry_date

            if expiry_date:
                expiry_date = expiry_date.replace(tzinfo=None)

            new_contract = Contract(
                title=contract_data.title,
                status=contract_data.status,
                department=contract_data.department,
                expiry_date=expiry_date,
                uploaded_by=user_id
            )

            session.add(new_contract)
            await session.commit()
            await session.refresh(new_contract)

            return new_contract
        finally:
            await close_connection(session)

    # -------------------------
    # DELETE CONTRACT
    # -------------------------
    @staticmethod
    async def delete_contract(contract_id: int):
        session = await create_connection()
        try:
            result = await session.execute(
                select(Contract).where(Contract.id == contract_id)
            )

            contract = result.scalar_one_or_none()

            if not contract:
                return None

            await session.delete(contract)
            await session.commit()

            return contract
        finally:
            await close_connection(session)

    # -------------------------
    # GET TOTAL ACTIVE CONTRACTS
    # -------------------------
    @staticmethod
    async def get_total_active_contracts():
        session = await create_connection()
        try:
            result = await session.execute(
                select(func.count(Contract.id)).where(Contract.status == "active", Contract.is_deleted == False)
            )
            return result.scalar()
        finally:
            await close_connection(session)

    # -------------------------
    # GET CONTRACTS EXPIRING THIS MONTH (within 30 days)
    # -------------------------
    @staticmethod
    async def get_expiring_this_month():
        session = await create_connection()
        try:
            now = datetime.utcnow()
            thirty_days = now + timedelta(days=30)
            result = await session.execute(
                select(Contract).where(
                    Contract.expiry_date >= now,
                    Contract.expiry_date <= thirty_days,
                    Contract.is_deleted == False
                )
            )
            return result.scalars().all()
        finally:
            await close_connection(session)

    # -------------------------
    # GET CONTRACTS EXPIRING NEXT QUARTER (within 90 days)
    # -------------------------
    @staticmethod
    async def get_expiring_next_quarter():
        session = await create_connection()
        try:
            now = datetime.utcnow()
            ninety_days = now + timedelta(days=90)
            result = await session.execute(
                select(Contract).where(
                    Contract.expiry_date >= now,
                    Contract.expiry_date <= ninety_days,
                    Contract.is_deleted == False
                )
            )
            return result.scalars().all()
        finally:
            await close_connection(session)

    # -------------------------
    # GET UPCOMING EXPIRATIONS LIST
    # -------------------------
    @staticmethod
    async def get_upcoming_expirations():
        session = await create_connection()
        try:
            now = datetime.utcnow()
            ninety_days = now + timedelta(days=90)
            result = await session.execute(
                select(Contract).where(
                    Contract.expiry_date >= now,
                    Contract.expiry_date <= ninety_days,
                    Contract.is_deleted == False
                ).order_by(Contract.expiry_date.asc())
            )
            contracts = result.scalars().all()

            return [
                {
                    "id": c.id,
                    "title": c.title,
                    "department": c.department,
                    "expiry_date": c.expiry_date,
                    "days_left": (c.expiry_date - now).days
                }
                for c in contracts
            ]
        finally:
            await close_connection(session)

    # -------------------------
    # GET CONTRACTS WITH FILTERS
    # -------------------------
    @staticmethod
    async def get_filtered_contracts(
        search: str | None = None,
        department: str | None = None,
        status: str | None = None
    ):
        session = await create_connection()
        try:
            query = select(Contract).where(Contract.is_deleted==False)

            if search:
                query = query.where(Contract.title.ilike(f"%{search}%"))

            if department:
                query = query.where(Contract.department == department)

            if status:
                query = query.where(Contract.status == status)

            result = await session.execute(query)
            return result.scalars().all()
        finally:
            await close_connection(session)

    # -------------------------
    # GET SINGLE CONTRACT BY ID
    # -------------------------
    @staticmethod
    async def get_contract_by_id(contract_id: int):
        session = await create_connection()
        try:
            result = await session.execute(
                select(Contract).where(
                    Contract.id == contract_id,
                    Contract.is_deleted == False
                    )
            )
            contract = result.scalar_one_or_none()
            return contract
        finally:
            await close_connection(session)

    # -------------------------
    # UPLOAD CONTRACT WITH AI
    # -------------------------
    @staticmethod
    async def upload_contract(
        title: str,
        department: str,
        user_id: int,
        file: UploadFile
    ):
        session = await create_connection()
        try:
            # Save file to disk
            file_path = await save_upload_file(file)

            # Extract text from file
            contract_text = extract_text_from_file(file_path)

            # Send text to Gemini AI
            ai_result = await analyze_contract(contract_text)

            # Parse dates from AI result
            start_date = None
            expiry_date = None

            if ai_result.get("start_date"):
                try:
                    start_date = datetime.strptime(
                        ai_result["start_date"], "%Y-%m-%d"
                    )
                except:
                    pass

            if ai_result.get("end_date"):
                try:
                    expiry_date = datetime.strptime(
                        ai_result["end_date"], "%Y-%m-%d"
                    )
                except:
                    pass

            # Save everything to DB
            new_contract = Contract(
                title=title,
                department=department,
                status="active",
                file_path=file_path,
                start_date=start_date,
                expiry_date=expiry_date,
                supplier=ai_result.get("supplier"),
                value=ai_result.get("value"),
                notice_period=ai_result.get("notice_period"),
                ai_summary=ai_result.get("ai_summary"),
                risk_flag=ai_result.get("risk_flag"),
                key_clauses=ai_result.get("key_clauses"),
                uploaded_by=user_id
            )

            session.add(new_contract)
            await session.commit()
            await session.refresh(new_contract)

            return new_contract

        finally:
            await close_connection(session)