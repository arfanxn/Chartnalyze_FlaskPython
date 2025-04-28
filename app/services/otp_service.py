from app.extensions import db
from app.models.otp import Otp
from app.exceptions.http_exception import HttpException
from app.helpers.mail_helpers import send_mail
from app.config import Config
from sqlalchemy import and_
from datetime import datetime
from http import HTTPStatus

class OtpService :
    def __init__(self):
        pass

    def send(self, email):
        try: 
            Otp.query.filter(Otp.email == email).update(
                {Otp.revoked_at: datetime.now()},
                synchronize_session=False
            )

            otp = Otp()
            otp.email = email
            db.session.add(otp)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise HttpException(message='OTP sent failed', status=HTTPStatus.INTERNAL_SERVER_ERROR)

        send_mail(
            subject=f"{Config.APP_NAME} | OTP",
            recipients=[otp.email],  # List of recipient email addresses
            body=f"Your OTP is [ {otp.code} ], valid for {otp.expiration_minutes()} minutes"
        )

        return otp

    def verify (self, email, code):
        otp = Otp.query.filter(
            and_(
                Otp.email == email,
                Otp.code == code,
                Otp.used_at == None,
                Otp.revoked_at == None,
                Otp.expired_at > datetime.now()
            )
        ).first()
                
        if otp == None: 
            raise HttpException(message='OTP is invalid', status=HTTPStatus.UNPROCESSABLE_ENTITY)
        
        otp.used_at = datetime.now()
        db.session.commit()