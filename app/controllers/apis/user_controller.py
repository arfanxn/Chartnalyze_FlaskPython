from app.exceptions.http_exception import HttpException
from app.exceptions.validation_exception import ValidationException
from app.extensions import db
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.update_user_form import UpdateUserForm
from app.helpers.response_helpers import create_response_tuple
from app.middlewares.authenticate_middleware import authenticate
from app.middlewares.verify_email_middleware import verify_email
from app.models.user import User
from datetime import timedelta
from flask import Blueprint, g, request
from flask_jwt_extended import create_access_token
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user by validating input and saving to the database.
    Returns a success message if successful, raises ValidationException if email exists.
    """
    form = RegisterForm(request.form) 
    form.try_validate()

    user = User()
    user.username = form.username.data
    user.email = form.email.data
    user.set_password(form.password.data)

    try:
        db.session.add(user)
        db.session.commit()    
    except IntegrityError as e:
        message = 'Email already exists' 
        errors = {'email': [message]}
        raise ValidationException(message, errors)

    return create_response_tuple(status=HTTPStatus.CREATED, message='User registered successfully')

@user_bp.route('/login', methods=['POST'])
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
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))

    return create_response_tuple(status=HTTPStatus.OK, message='User logged in successfully', data={'access_token': access_token})

@user_bp.route('/logout', methods=['DELETE'])
@authenticate
@verify_email
def logout():
    """
    Logs out the authenticated user and returns a success message.
    """
    return create_response_tuple(status=HTTPStatus.OK, message='User logged out successfully')

@user_bp.route("/users/<string:user_identifier>", methods=["GET"])
@authenticate
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

@user_bp.route("/users/self", methods=["GET"])
@authenticate
@verify_email
def showSelf():
    """
    Retrieves the currently authenticated user's data.
    """
    user: User = g.user
    return show(user.id)

@user_bp.route("/users/<string:user_id>", methods=["PUT"])
@authenticate
@verify_email
def update(user_id: str):
    """
    Updates user details by validating input. Returns updated user data or raises HttpException if not found.
    """
    form = UpdateUserForm(request.form) 
    form.try_validate()

    user: User = User.query.filter_by(id=user_id).first()
    if user is None:
        raise HttpException(message='User not found', status=HTTPStatus.NOT_FOUND)
    
    user.name = form.name.data if form.name.data else user.name
    user.username = form.username.data if form.username.data else user.username
    user.birth_date = form.birth_date.data if form.birth_date.data else user.birth_date

    db.session.commit()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User updated successfully',
        data={'user': user.to_json()}
    )

@user_bp.route("/users/self", methods=["PUT"])
@authenticate
@verify_email
def updateSelf():
    """
    Updates the currently authenticated user's details.
    """
    user = g.user
    return update(user.id)
