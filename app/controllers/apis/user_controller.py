from app.exceptions.http_exception import HttpException
from app.exceptions.validation_exception import ValidationException
from app.extensions import db
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.update_user_form import UpdateUserForm
from app.helpers.response_helpers import create_response_tuple
from app.middlewares.authenticate_middleware import authenticate
from app.models.user import User
from flask import Blueprint, g, request
from flask_jwt_extended import create_access_token
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user in the system.

    This function handles the registration of a new user by validating the
    input data from the request form. If the provided data is valid, it creates
    a new user instance, hashes the user's password, and attempts to save the
    user in the database. If the email already exists, a ValidationException
    is raised.

    Returns:
        A JSON response containing a success message and HTTP status code 201
        if registration is successful.

    Raises:
        ValidationException: If the form validation fails or the email already exists.
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

    return create_response_tuple(status=HTTPStatus.CREATED, message='User registered successfully',)

@user_bp.route('/login', methods=['POST'])
def login():
    """
    Handles user login.

    This function validates the input data from the request form. If the
    provided data is valid, it attempts to find a user in the database by
    either username or email. If the user is found and the passwords match,
    it generates a JWT token and returns it in the response.

    Returns:
        A JSON response containing a success message, HTTP status code 200,
        and the generated JWT token if the login is successful.

    Raises:
        ValidationException: If the form validation fails or the credentials
            do not match.
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
    
    access_token = create_access_token(identity=user.id)

    return create_response_tuple(status=HTTPStatus.OK, message='User logged in successfully', data={'access_token': access_token})

@user_bp.route('/logout', methods=['DELETE'])
@authenticate
def logout():
    """
    Logs out the currently authenticated user.

    This function handles the logout process for an authenticated user.
    It requires the user to be authenticated via the `authenticate` decorator.
    Upon successful logout, it returns a success message with an HTTP status code 200.

    Returns:
        A JSON response containing a success message and HTTP status code 200.
    """
    return create_response_tuple(status=HTTPStatus.OK, message='User logged out successfully')

@user_bp.route("/users/self", methods=["GET"])
@authenticate
def self():
    """
    Returns the currently authenticated user.

    This function is a shortcut for getting the currently authenticated user.
    It returns the user that is currently authenticated via the `authenticate`
    decorator.

    Returns:
        A JSON response containing a success message, HTTP status code 200,
        and the user data if the request is successful.
    """
    user: User = g.user
    return show(user.id)

@user_bp.route("/users/<string:user_id>", methods=["GET"])
@authenticate
def show(user_id: str):
    """
    Returns the user with the given ID.

    This function handles the retrieval of a user by ID. It requires the user
    to be authenticated via the `authenticate` decorator.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        A JSON response containing a success message, HTTP status code 200,
        and the user data if the request is successful.
    """

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        raise HttpException(message='User not found', status=HTTPStatus.NOT_FOUND)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='User found successfully',
        data={'user': user.to_json()}
    )

@user_bp.route("/users/self", methods=["PUT"])
@authenticate
def updateSelf():
    user = g.user
    return update(user.id)

@user_bp.route("/users/<string:user_id>", methods=["PUT"])
@authenticate
def update (user_id: str):
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
