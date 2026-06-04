from sqlalchemy import select , delete
from app.db.db import create_connection, close_connection
from app.db.models import Contract
from app.model.models import ContractCreate
from app.db.models import Contract


class ContractService:

    # -------------------------
    # GET ALL CONTRACTS
    # -------------------------
    @staticmethod
    async def get_all_contracts():
        session = await create_connection()
        try:
            result = await session.execute(
                select(Contract)
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