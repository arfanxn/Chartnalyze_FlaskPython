from datetime import datetime, timedelta
from flask import Blueprint, g, request
from flask_jwt_extended import create_access_token
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.config import Config
from app.exceptions import HttpException, ValidationException
from app.extensions import db, limiter
from app.forms import (
    LoginForm,
    OtpCodeForm,
    RegisterForm,
    ResetUserPasswordForm,
    UpdateUserEmailForm,
    UpdateUserForm,
    UpdateUserPasswordForm,
)
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import (
    authenticate,
    authorize,
    verify_email
)
from app.models.user import User
from app.services.otp_service import OtpService

otp_service = OtpService()
user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user by validating input and saving to the database.
    Returns a success message if successful, raises ValidationException if email exists.
    """
    form = RegisterForm(request.form) 
    form.try_validate()

    user = User()
    user.name = form.name.data
    user.username = form.username.data
    user.birth_date = form.birth_date.data
    user.email = form.email.data
    user.password = form.password.data 

    try:
        db.session.add(user)
        db.session.commit()    
    except IntegrityError as e:
        message = 'Email or username already exists' 
        errors = {'email': [message]}
        raise ValidationException(message, errors)

    return create_response_tuple(
        status=HTTPStatus.CREATED, 
        message='User registered successfully', 
        data={'user': user.to_json()})

@user_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """
    Handles user login by validating credentials and returning a JWT token if successful.
    Raises ValidationException if credentials do not match.
    """
    form = LoginForm(request.form)
    form.try_validate()
    
    user = User.query.filter(
        (User.email == form.identifier.data) | 
        (User.username == form.identifier.data)
    ).first()

    if (user is None) or (user.check_password(form.password.data) == False):
        message = 'Credentials do not match'
        errors = {'password': [message]}
        raise ValidationException(message, errors)
    
    # Generate a JWT token with the user's ID as the identity and 30 days expiration time.
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=Config.JWT_EXPIRATION_DAYS))

    return create_response_tuple(status=HTTPStatus.OK, message='User logged in successfully', data={'access_token': access_token})

@user_bp.route('/self/email/verify', methods=['POST'])
@authenticate
def verify_self_email():
    form = OtpCodeForm(request.form)
    form.try_validate()
    
    try:
        otp_service.verify(email=g.user.email, code=form.code.data)

        user:User = g.user
        user.email_verified_at = datetime.now()
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise HttpException(message='Email verification failed', status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return create_response_tuple(status=HTTPStatus.OK, message='Email verified successfully')

@user_bp.route('/self/logout', methods=['DELETE'])
@limiter.limit("10 per minute")
@authenticate
def logout():
    """
    Logs out the authenticated user and returns a success message.
    """
    return create_response_tuple(status=HTTPStatus.OK, message='User logged out successfully')

@user_bp.route("/<string:user_identifier>", methods=["GET"])
@authenticate
@authorize('users.show')
@verify_email
def show(user_identifier: str):
    """
    Retrieves the user by ID or email/username. Returns user data or raises HttpException if not found.
    """
    user = User.query.filter(
        (User.id == user_identifier) | 
        (User.email == user_identifier) | 
        (User.username == user_identifier)
    ).first()
    if user is None:
        raise HttpException(message='User not found', status=HTTPStatus.NOT_FOUND)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User found successfully',
        data={'user': user.to_json()}
    )

@user_bp.route("/self", methods=["GET"])
@authenticate
def show_self():
    """
    Retrieves the currently authenticated user's data.
    """
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User found successfully',
        data={'user': g.user.to_json()}
    )

def _update(user_id: str):
    form = UpdateUserForm(request.form) 
    form.try_validate()

    user: User = User.query.filter_by(id=user_id).first()
    if user is None:
        raise HttpException(message='User not found', status=HTTPStatus.NOT_FOUND)
        
    user.name = form.name.data
    if form.username.data != user.username: # TODO: fix bug on updating username with the same username occurs error
        user.username = form.username.data
    user.birth_date = form.birth_date.data

    try:
        db.session.commit()
    except IntegrityError as e:
        message = 'Username already exists' 
        errors = {'username': [message]}
        raise ValidationException(message, errors)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User updated successfully',
        data={'user': user.to_json()}
    )

@user_bp.route("/<string:user_id>", methods=["PUT"])
@authenticate
@authorize('users.update')
@verify_email
def update(user_id: str):
    return _update(user_id)

@user_bp.route("/self", methods=["PUT"])
@authenticate
@verify_email
def update_self():
    """
    Updates the currently authenticated user's details.
    """
    user = g.user
    return _update(user.id)

@user_bp.route("/self/email", methods=["PATCH"])
@authenticate
@verify_email
def update_self_email():
    """
    Updates the currently authenticated user's email address by validating input and sending an OTP code to the old email.
    Returns updated user data or raises HttpException if not found.

    Args:
        request.form (dict): request form containing form data

    Returns:
        A response tuple containing the HTTP status and response message.
    """
    form = UpdateUserEmailForm(request.form)
    form.try_validate()
    
    old_email = g.user.email
    new_email = form.email.data

    otp_service.verify(email=old_email, code=form.code.data)   

    user: User = g.user
    user.email = new_email
    user.email_verified_at = None
    db.session.commit()

    return create_response_tuple(
        status=HTTPStatus.OK, 
        message='Email updated successfully, please verify your new email', 
        data={'user': user.to_json()}
    )

@user_bp.route("/self/password", methods=["PATCH"])
@authenticate
@verify_email
def update_self_password():
    """
    Updates the currently authenticated user's password by validating input and verifying the current password.
    Returns a success message if successful, raises ValidationException if current password does not match.
    """
    form = UpdateUserPasswordForm(request.form)
    form.try_validate()
    
    user: User = g.user

    if (user.check_password(form.current_password.data) == False):
        message = 'Current password does not match'
        errors = {'current_password': [message]}
        raise ValidationException(message, errors)

    user.password = form.password.data
    db.session.commit()

    return create_response_tuple(
        status=HTTPStatus.OK, 
        message='Password updated successfully',
    )


@user_bp.route("/self/password/reset", methods=["PATCH"])
@authenticate
def reset_self_password():
    """
    Resets the currently authenticated user's password by validating input and verifying an OTP code sent to the user's email.
    Returns a success message if successful, raises ValidationException if OTP code does not match.
    """
    form = ResetUserPasswordForm(request.form)
    form.try_validate()
    
    user: User = g.user

    otp_service.verify(email=user.email, code=form.code.data)

    user.password = form.password.data
    db.session.commit()

    return create_response_tuple(
        status=HTTPStatus.OK, 
        message='Password updated successfully',
    )

