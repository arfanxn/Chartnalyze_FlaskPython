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
from app.extensions import db
from app.enums.role_enums import RoleName
from app.enums.media_enums import ModelType
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound, UnprocessableEntity
from werkzeug.datastructures import FileStorage
from app.helpers.file_helpers import get_file_size, get_file_extension
from flask_jwt_extended import create_access_token
from datetime import timedelta, datetime
import ulid
import os

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