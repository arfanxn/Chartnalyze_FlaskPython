from app.middlewares import api_key_verified
from app.services.otp_service import OtpService 
from app.extensions import limiter
from app.forms import SendOtpForm
from app.helpers.response_helpers import create_response_tuple
from flask import Blueprint, request
from http import HTTPStatus

otp_service = OtpService()

otp_bp = Blueprint('otp', __name__)

@otp_bp.route('/otps/send', methods=['POST'])
@api_key_verified
@limiter.limit("1 per minute")
def send():
    form = SendOtpForm(request.form)
    form.try_validate()

    otp_service.send(form)
    
    return create_response_tuple(status=HTTPStatus.OK, message=f"OTP sent successfully")