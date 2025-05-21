from app.actions.action import Action   
from app.models import Otp
from app.extensions import db
from app.exceptions import HttpException, ValidationException
from app.helpers.mail_helpers import send_mail
from app.config import Config
from sqlalchemy import and_
from datetime import datetime
from http import HTTPStatus

class VerifyOtpAction (Action):
    def __init__(self):
        super().__init__()

    def __call__(self, email: str, code: int) -> tuple[Otp, bool]:
        otp = Otp.query.filter(
            and_(
                Otp.email == email,
                Otp.code == code,
                Otp.used_at == None,
                Otp.revoked_at == None,
                Otp.expired_at > datetime.now()
            )
        ).first()

        if otp is None: 
            message='Code is invalid'
            status=HTTPStatus.UNPROCESSABLE_ENTITY
            raise HttpException(message=message, status=status, additionals={'errors': {'code': [message]}})

        otp.used_at = datetime.now()

        return otp, True
