import requests
from flask import Blueprint, g, request, session, redirect
from http import HTTPStatus
from app.extensions import limiter
from app import extensions 
from app.config import Config
from app.forms import (
    LoginForm,
    OtpCodeForm,
    RegisterForm,
    ResetUserPasswordForm,
    UpdateUserEmailForm,
    UpdateUserForm,
    UpdateUserPasswordForm,
)
from app.resources import UserResource
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, authorized, api_key_verified, email_verified
from app.services import UserService
from app.enums.permission_enums import PermissionName

user_service = UserService()

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['POST'])
@api_key_verified
def register():
    """
    Registers a new user by validating input and saving to the database.
    Returns a success message if successful, raises UnprocessableEntity if email exists.
    """
    form = RegisterForm(request.form) 
    form.try_validate()

    user, = user_service.register(form)
    user_json = UserResource(user).to_json()

    return create_response_tuple(
        status=HTTPStatus.CREATED, 
        message='User registered successfully', 
        data={'user': user_json})

@user_bp.route('/login', methods=['POST'])
@api_key_verified
@limiter.limit("10 per minute")
def login():
    """
    Handles user login by validating credentials and returning a JWT token if successful.
    Raises UnprocessableEntity if credentials do not match.
    """
    form = LoginForm(request.form)
    form.try_validate()

    _, access_token = user_service.login(form)

    return create_response_tuple(status=HTTPStatus.OK, message='User logged in successfully', data={'access_token': access_token})

@user_bp.route('/login/google')
def login_google():
    authorization_url, state = extensions.flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='select_account'  # Force account selection
    )
    session['google_oauth2'] = {'state': state}


    print('authorization_url')
    print(authorization_url)

    return redirect(authorization_url)

@user_bp.route('/login/google/authorized', methods=['GET', 'POST'])
def login_google_authorized():
    _, access_token = user_service.login_google_authorized()
    return create_response_tuple(status=HTTPStatus.OK, message='User logged in with Google successfully', data={'access_token': access_token})

@user_bp.route('/self/email/verify', methods=['POST'])
@api_key_verified
@authenticated
def verify_self_email():
    form = OtpCodeForm(request.form)
    form.try_validate()
    
    email = g.user.email

    user, = user_service.verify_email(form=form, email=email)
    user_json = UserResource(user).to_json()

    return create_response_tuple(status=HTTPStatus.OK, message='Email verified successfully', data={'user': user_json})

@user_bp.route('/self/logout', methods=['DELETE'])
@api_key_verified
@limiter.limit("10 per minute")
@authenticated
def logout():
    """
    Logs out the authenticated user and returns a success message.
    """
    user_service.logout()
    return create_response_tuple(status=HTTPStatus.OK, message='User logged out successfully')

@user_bp.route("/reset-password", methods=["PATCH"])
@api_key_verified
def reset_password():
    form = ResetUserPasswordForm(request.form)
    form.try_validate()

    user_service.reset_password(form)

    return create_response_tuple(
        status=HTTPStatus.OK, 
        message='Password updated successfully',
    )

@user_bp.route("", methods=["GET"])
@api_key_verified
@authenticated
@authorized(PermissionName.USERS_INDEX.value)
@email_verified
def index():
    users, meta = user_service.paginate()
    users_json = UserResource.collection(users)
    users_pagination = {'users': users_json, **meta}

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Users paginated successfully',
        data={ **users_pagination }
    )

@user_bp.route("/<string:user_identifier>", methods=["GET"])
@api_key_verified
@authenticated
@authorized(PermissionName.USERS_SHOW.value)
@email_verified
def show(user_identifier: str):
    """
    Retrieves the user by ID or email/username. Returns user data or raises NotFound if not found.
    """
    user, = user_service.show(user_identifier=user_identifier)
    user_json = UserResource(user).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User found successfully',
        data={'user': user_json}
    )

@user_bp.route("/self", methods=["GET"])
@api_key_verified
@authenticated
def show_self():
    """
    Retrieves the currently authenticated user's data.
    """
    user_id = g.user.id

    user, = user_service.show(user_identifier=user_id)
    user_json = UserResource(user).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User found successfully',
        data={'user': user_json}
    )

@user_bp.route("/<string:user_id>", methods=["PUT"])
@api_key_verified
@authenticated
@authorized(PermissionName.USERS_UPDATE.value)
@email_verified
def update(user_id: str):
    form = UpdateUserForm(request.form) 
    form.try_validate()

    user, = user_service.update(form=form, user_id=user_id)
    user_json = UserResource(user).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User updated successfully',
        data={'user': user_json}
    )

@user_bp.route("/self", methods=["PUT"])
@api_key_verified
@authenticated
@email_verified
def update_self():
    """
    Updates the currently authenticated user's details.
    """
    form = UpdateUserForm(request.form) 
    form.try_validate()

    user_id = g.user.id

    user, = user_service.update(form=form, user_id=user_id) 
    user_json = UserResource(user).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User updated successfully',
        data={'user': user_json}
    )

@user_bp.route("/self/avatar", methods=["PATCH"])
@api_key_verified
@authenticated
@email_verified 
def update_self_avatar():
    avatar = request.files.get('avatar')

    user_id = g.user.id

    user, = user_service.update_avatar(avatar=avatar, user_id=user_id)
    user_json = UserResource(user).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK, 
        message='Avatar updated successfully', 
        data={'user': user_json }
    )   

@user_bp.route("/self/email", methods=["PATCH"])
@api_key_verified
@authenticated
@email_verified
def update_self_email():
    """
    Updates the currently authenticated user's email address by validating input and sending an OTP code to the old email.

    Args:
        request.form (dict): request form containing form data

    Returns:
        A response tuple containing the HTTP status and response message.
    """
    form = UpdateUserEmailForm(request.form)
    form.try_validate()

    user, = user_service.update_email(form=form, user_id=g.user.id)
    user_json = UserResource(user).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK, 
        message='Email updated successfully', 
        data={'user': user_json}
    )

@user_bp.route("/self/password", methods=["PATCH"])
@api_key_verified
@authenticated
@email_verified
def update_self_password():
    """
    Updates the currently authenticated user's password by validating input and verifying the current password.
    Returns a success message if successful, raises UnprocessableEntity if current password does not match.
    """
    form = UpdateUserPasswordForm(request.form)
    form.try_validate()

    user_id = g.user.id
    
    user_service.update_password(form=form, user_id=user_id)

    return create_response_tuple(
        status=HTTPStatus.OK, 
        message='Password updated successfully',
    )