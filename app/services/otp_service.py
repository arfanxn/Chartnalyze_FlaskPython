from app.services import Service
from app.extensions import db
from app.models.otp import Otp
from app.exceptions import HttpException
from app.helpers.mail_helpers import send_mail
from app.actions import SendOtpAction, VerifyOtpAction
from app.forms import SendOtpForm
from app.config import Config
from sqlalchemy import and_
from datetime import datetime
from http import HTTPStatus

class OtpService(Service):

    def __init__(self):
        super().__init__()
    
    def send(self, form: SendOtpForm):
        send_otp = SendOtpAction()
        send_otp(email=form.email.data)

        db.session.commit()

