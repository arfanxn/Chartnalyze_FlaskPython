from app.services import Service
from app.helpers.mail_helpers import send_mail
from app.actions import SendOtpAction
from app.forms import SendOtpForm

class OtpService(Service):

    def __init__(self):
        super().__init__()
    
    def send(self, form: SendOtpForm):
        send_otp = SendOtpAction()
        send_otp(email=form.email.data)