import ulid
import os
import requests
import re
import random
from datetime import timedelta, datetime
from flask import session, request
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound, UnprocessableEntity, Unauthorized
from werkzeug.datastructures import FileStorage
from app.helpers.file_helpers import get_file_size, get_file_extension
from app.config import Config
from app.repositories import UserRepository
from app.services import Service
from app.actions import VerifyOtpAction
from app.forms import (
    RegisterForm,
    LoginForm,
    OtpCodeForm,
    ResetUserPasswordForm, 
    UpdateUserForm,
    UpdateUserEmailForm,
    UpdateUserPasswordForm
)
from app.models import User, Role, Media
from app.extensions import db, flow
from app.enums.role_enums import RoleName
from app.enums.media_enums import ModelType

user_repository = UserRepository()

class UserService(Service):
    def __init__(self):
        super().__init__()

    def register(self, form: RegisterForm) -> tuple[User]: 
        try:
            role = Role.query.filter_by(name=RoleName.USER.value).first()

            user = User()
            user.name = form.name.data
            user.username = form.username.data
            user.birth_date = form.birth_date.data
            user.email = form.email.data
            user.password = form.password.data 
            user.roles.extend([role]) 
            db.session.add(user)

            db.session.commit()    

            return (user, )
        except IntegrityError as e:
            raise UnprocessableEntity({'email' : ['Email or username already exists']})

    def login(self, form: LoginForm) -> tuple[User, str]:
        user = User.query.filter(
            (User.email == form.identifier.data) | 
            (User.username == form.identifier.data)
        ).first()

        if (user is None) or (user.check_password(form.password.data) == False):
            raise UnprocessableEntity({'password': ['Credentials do not match']})
        
        # Generate a JWT token with the user's ID as the identity and 30 days expiration time.
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=Config.JWT_EXPIRATION_DAYS))

        return (user, access_token)
    
    def login_google_authorized(self) -> tuple[User, str]:
        """
        Handles Google OAuth2 authorization callback.
        Fetches the authorization token from the flow object, then uses it to fetch user info from Google.
        If the user does not exist in the database, creates a new user with the email and username fields.
        Returns a tuple containing the user and the JWT access token.
        """
        flow.fetch_token(authorization_response=request.url)
        
        credentials = flow.credentials
        session['google_oauth2'] = {'credentials': {'token': credentials.token}}
        
        user_json = requests.get(
            Config.GOOGLE_OATUH_USERINFO_URI,
            headers={'Authorization': f'Bearer {credentials.token}'}
        ).json()

        email = user_json.get('email')
        user = User.query.filter(User.email == email).first()

        if user is None:
            role = Role.query.filter_by(name=RoleName.USER.value).first()

            name = user_json.get('name')
            username = re.sub(r'\s+', '_', name[:12]).lower() + str(random.randrange(1000, 9999, 1))
            
            user = User()
            user.email = email
            user.name = name
            user.username = username
            user.password = None
            user.roles.extend([role])

            db.session.add(user)
            db.session.commit()    

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=Config.JWT_EXPIRATION_DAYS))
        
        return (user, access_token)
        

    def verify_email (self, form: OtpCodeForm, email: str) -> tuple[User]: 
        try:
            verify_otp = VerifyOtpAction()
            otp, _ = verify_otp(email=email, code=form.code.data)

            user:User = User.query.filter_by(email=email).first()
            user.email_verified_at = datetime.now()

            db.session.commit()

            return (user, )
        except SQLAlchemyError as e:
            db.session.rollback()
            raise InternalServerError('Email verification failed')
        
    def logout (self) -> tuple[bool]:
        """
        Revoke the current user's Google OAuth token and clear the session.

        Returns:
            tuple[bool]: (True, ) if the logout was successful, otherwise an InternalServerError will be raised.
        """
        try:
            token = session['google_oauth2']['credentials']['token']
        except KeyError:
            token = None
        if token:
            requests.post(
                Config.GOOGlE_OAUTH_REVOKE_URI, 
                params={'token': token}, 
                headers={'content-type': 'application/x-www-form-urlencoded'}
            )

        session.clear()
        return (True, )
        
    def reset_password(self, form: ResetUserPasswordForm) -> tuple[User]:
        try:
            verify_otp = VerifyOtpAction()
            otp, _ = verify_otp(form.email.data, form.code.data)

            user = User.query.filter_by(email=form.email.data).first()  
            user.password = form.password.data

            db.session.commit()

            return (user, )
        except SQLAlchemyError as e:
            db.session.rollback()
            raise InternalServerError('Password reset failed')
        
    def paginate (self) -> tuple[list[User], dict]:
        users, meta = user_repository.paginate()
        return (users, meta)
    
    def show(self, user_identifier: str) -> tuple[User]:
        user, = user_repository.show(user_identifier=user_identifier)
        if user is None:
            raise NotFound('User not found')

        return (user, )
    
    def update(self, form: UpdateUserForm, user_id: str) -> tuple[User]:
        user: User = User.query.filter_by(id=user_id).first()
        if user is None:
            raise NotFound('User not found')
            
        if form.name.data != user.name:
            user.name = form.name.data
        if form.username.data != user.username: 
            user.username = form.username.data
        if form.birth_date.data != user.birth_date:
            user.birth_date = form.birth_date.data

        try:
            db.session.commit()
        except IntegrityError as e:
            raise UnprocessableEntity({'email' : ['Username already exists']})

        return (user, )

    def update_avatar (self, avatar: (FileStorage | None), user_id: str) -> tuple[User]:
        user = User.query.options(db.joinedload(User.avatar)).filter(User.id==user_id).first()
        if user is None:
            raise NotFound('User not found')
        
        if user.avatar is None:
            user.avatar = Media(
                model_id=user_id,
                model_type=ModelType.USER.value,
                collection_name='avatar'
            )
        
        file_extension = get_file_extension(file=avatar)
        file_size = get_file_size(file=avatar)
        media_file_name = ulid.new().str + file_extension

        user.avatar.name = avatar.filename
        user.avatar.file_name = media_file_name 
        user.avatar.mime_type = avatar.mimetype
        user.avatar.size = file_size

        avatar.save(os.path.join(Config.UPLOAD_FOLDER, 'images/avatars', media_file_name))

        db.session.commit()

        return (user, )

    def update_email (self, form: UpdateUserEmailForm, user_id: str) -> tuple[User] :
        new_email = form.email.data

        verify_otp = VerifyOtpAction()
        verify_otp(email=new_email, code=form.code.data)

        user: User = User.query.filter_by(id=user_id).first()
        user.email = new_email
        user.email_verified_at = datetime.now()
        
        try: 
            db.session.commit()
        except IntegrityError as e: 
            raise UnprocessableEntity({'email' : ['Email already exists']})

        return (user, )

    def update_password (self, form: UpdateUserPasswordForm, user_id: str) -> tuple[User]:
        user: User = User.query.filter_by(id=user_id).first()

        if (user.check_password(form.current_password.data) == False):
            raise UnprocessableEntity({'current_password': ['Current password does not match']})

        user.password = form.password.data
        
        db.session.commit()

        return (user, )