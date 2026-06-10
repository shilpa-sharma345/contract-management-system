from datetime import datetime, timedelta
from sqlalchemy import select
from app.db.db import create_connection, close_connection
from app.db.models import Contract, User
from app.services.email_service import send_email


class ReminderService:

    @staticmethod
    async def send_expiry_reminders(days_before: int):

        session = await create_connection()

        try:
            print("Reminder job started")

            today = datetime.utcnow().date()
            target_date = today + timedelta(days=days_before)

            result = await session.execute(
                select(Contract).where(
                    Contract.expiry_date.isnot(None),
                    Contract.is_deleted == False
                )
            )

            contracts = result.scalars().all()

            for contract in contracts:
                if not contract.expiry_date:
                    continue

                expiry = contract.expiry_date.date()

                if expiry != target_date:
                    continue

                print("MATCH FOUND:", contract.title)

                user_result = await session.execute(
                    select(User).where(User.id == contract.uploaded_by)
                )
                user = user_result.scalar_one_or_none()

                if not user:
                    print("User not found")
                    continue

                # Urgency config
                if days_before == 1:
                    badge_color = "#DC2626"
                    badge_text = "URGENT — 1 Day Left"
                    urgency_msg = "This contract expires tomorrow. Immediate action is required."
                elif days_before == 7:
                    badge_color = "#EA580C"
                    badge_text = "7 Days Remaining"
                    urgency_msg = "This contract expires in 7 days. Please begin the renewal process."
                else:
                    badge_color = "#CA8A04"
                    badge_text = "30 Days Remaining"
                    urgency_msg = "This contract expires in 30 days. Now is a good time to review and plan renewal."

                template_data = {
                    "user_name": user.full_name,
                    "badge_color": badge_color,
                    "badge_text": badge_text,
                    "urgency_msg": urgency_msg,
                    "contract_title": contract.title,
                    "department": contract.department or "N/A",
                    "supplier": contract.supplier or "N/A",
                    "value": contract.value or "N/A",
                    "expiry_date": expiry.strftime("%d %B %Y"),
                    "notice_period": contract.notice_period or "N/A",
                }

                success = send_email(
                    to_email=user.email,
                    subject=f"⚠️ Contract Expiry Alert — {contract.title} ({days_before} day{'s' if days_before > 1 else ''} left)",
                    template_data=template_data
                )

                print("EMAIL SUCCESS:", success)

        finally:
            await close_connection(session)