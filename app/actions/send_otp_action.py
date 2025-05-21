from app.actions.action import Action   
from app.models import Otp
from app.extensions import db
from app.exceptions import HttpException, ValidationException
from app.helpers.mail_helpers import send_mail
from app.config import Config
from sqlalchemy import and_
from datetime import datetime
from http import HTTPStatus
import threading

class SendOtpAction (Action):
    def __init__(self):
        super().__init__()

    def __call__(self, email: str) -> tuple[Otp]:
        try: 
            revoked_otp = Otp.query.filter(Otp.email == email).first()
            revoked_otp.revoked_at = datetime.now()

            otp = Otp()
            otp.email = email
            db.session.add(otp)
        except Exception as e:
            db.session.rollback()
            raise HttpException(message='OTP sent failed', status=HTTPStatus.INTERNAL_SERVER_ERROR)

        send_email_async = lambda: send_mail(
            subject=f"{Config.APP_NAME} | OTP",
            recipients=[otp.email],  # List of recipient email addresses
            body=f"Your OTP is [ {otp.code} ], valid for {otp.expiration_minutes} minutes"
        )
        email_thread = threading.Thread(target=send_email_async)
        email_thread.start()

        return (otp, )
