from app.actions.action import Action   
from app.models import Otp
from werkzeug.exceptions import UnprocessableEntity
from sqlalchemy import and_
from datetime import datetime

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
            raise UnprocessableEntity({'code': ['Code is invalid']})

        otp.used_at = datetime.now()

        return otp, True
