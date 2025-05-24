from app.actions.action import Action
from app.models import Otp
from app.extensions import db
from app.helpers.mail_helpers import send_mail
from app.config import Config
from werkzeug.exceptions import InternalServerError
from datetime import datetime
from http import HTTPStatus
import threading
from flask import current_app

class SendOtpAction(Action):
    def __init__(self):
        super().__init__()

    def __call__(self, email: str) -> tuple[Otp]:
        try:
            # Revoke previous OTP if exists
            revoked_otp = Otp.query.filter(Otp.email == email).first()
            if revoked_otp:
                revoked_otp.revoked_at = datetime.now()

            # Create a new OTP
            otp = Otp(email=email)
            db.session.add(otp)
            db.session.commit()

            # Capture needed data BEFORE thread starts
            otp_data = {
                "email": otp.email,
                "code": otp.code,
                "expiration_minutes": otp.expiration_minutes
            }

        except Exception as e:
            db.session.rollback()
            raise InternalServerError(description='OTP sent failed', original_exception=e)

        # Get actual app object
        app = current_app._get_current_object()

        def send_email_async(app, otp_data):
            with app.app_context():
                try:
                    # Re-query the OTP within the new context if needed
                    # Or use the otp_data directly
                    send_mail(
                        subject=f"{Config.APP_NAME} | OTP",
                        recipients=[otp_data["email"]],
                        body=f"Your OTP is [ {otp_data['code']} ], valid for {otp_data['expiration_minutes']} minutes"
                    )
                except Exception as e:
                    app.logger.error(f"Failed to send email: {str(e)}")

        # Pass the captured data to the thread
        email_thread = threading.Thread(
            target=send_email_async,
            args=(app, otp_data)
        )
        email_thread.start()

        return (otp, )