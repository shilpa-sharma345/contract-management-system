import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, DynamicTemplateData
from app.constants.environ import SENDGRID_API_KEY, FROM_EMAIL, SENDGRID_TEMPLATE_ID

logger = logging.getLogger(__name__)


def send_email(
    to_email: str,
    subject: str,
    template_data: dict,
) -> bool:
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject=subject
        )

        message.template_id = SENDGRID_TEMPLATE_ID
        message.dynamic_template_data = template_data

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        print("SENDGRID STATUS:", response.status_code)

        return response.status_code in [200, 202]

    except Exception as e:
        logger.error(f"SendGrid error: {str(e)}")
        return False