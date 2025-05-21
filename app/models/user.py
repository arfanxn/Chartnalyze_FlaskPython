from app.extensions import db
from app.enums.notification_enums import NotifiableType
from app.enums.media_enums import ModelType  
from app.helpers.string_helpers import is_ulid
from datetime import datetime
import bcrypt
import ulid

# ==========================================
# User Model Definition
# ==========================================
class User(db.Model):
    __tablename__ = 'users'

    # ==========================================
    # Columns Definition
    # ==========================================
    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    country_id = db.Column(db.CHAR(26), db.ForeignKey('countries.id'))
    name = db.Column(db.String(50))
    username = db.Column(db.String(16), nullable=False, unique=True)
    birth_date = db.Column(db.Date)
    email = db.Column(db.String(50), nullable=False, unique=True)
    email_verified_at = db.Column(db.DateTime)
    _password = db.Column('password', db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    country = db.relationship('Country', back_populates='users')
    roles = db.relationship(
        'Role', 
        secondary='role_user',  # Use table name as string
        back_populates='users',  # Match the name in Role model
    )
    notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.notifiable_id",
        primaryjoin="and_(User.id == Notification.notifiable_id,Notification.notifiable_type == '{}')".format(NotifiableType.USER.value),    
        back_populates="notifiable_user",
        overlaps="notifiable_role,notifications"
    )
    follower_users = db.relationship(
        'User',
        secondary='follows',
        primaryjoin="User.id == Follow.followed_id",
        secondaryjoin="Follow.follower_id == User.id",
        viewonly=True,
    )
    followed_users = db.relationship(
        'User',
        secondary='follows',
        primaryjoin="User.id == Follow.follower_id",
        secondaryjoin="Follow.followed_id == User.id",
        viewonly=True,
    )
    posts = db.relationship('Post', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    likes = db.relationship('Like', back_populates='user')
    saves = db.relationship('Save', back_populates='user')
    medias = db.relationship(
        'Media',
        foreign_keys='Media.model_id',
        primaryjoin="and_(User.id == Media.model_id, Media.model_type == '{}')".format(ModelType.USER.value),
        overlaps="medias"
    )
    avatar = db.relationship(
        'Media',
        foreign_keys='Media.model_id',
        primaryjoin="and_(User.id == Media.model_id, Media.model_type == '{}', Media.collection_name == 'avatar')".format(ModelType.USER.value),
        overlaps="medias",
        uselist=False
    )

    # ==========================================
    # Password Handling
    # ==========================================
    @property
    def password(self):
        """Returns the hashed password."""
        return self._password

    @password.setter
    def password(self, password):
        """Hashes and sets the password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self._password = hashed_password

    def check_password(self, password):
        """Checks if the provided password matches the stored hashed password."""
        return bcrypt.checkpw(password.encode('utf-8'), self._password)

    # ==========================================
    # Permission Checking
    # ==========================================
    def has_permissions(self, *permissions) -> bool:
        """
        Check if the user has ANY of the specified permissions.
        Accepts: Permission names (str), IDs (str), or Permission instances.
        Returns: True/False (executed at the database level).
        """
        if not permissions:
            return False  # Edge case: no permissions specified

        # LOCAL IMPORT to break circular dependency
        from app.models import Permission, PermissionRole, RoleUser

        names, ids = set(), set()
        for perm in permissions:
            if isinstance(perm, Permission):
                ids.add(perm.id)
            elif isinstance(perm, str):
                if is_ulid(perm):  # detects if ulid
                    ids.add(perm)
                else:
                    names.add(perm)

        # Query to check if any permission matches
        query = db.session.query(db.exists().where(
            db.and_(
                RoleUser.user_id == self.id,
                RoleUser.role_id == PermissionRole.role_id,
                PermissionRole.permission_id == Permission.id,
                db.or_(
                    Permission.id.in_(ids),
                    Permission.name.in_(names)
                )
            )
        ))
        return db.session.scalar(query)

    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        """Convert the User model instance to a JSON-serializable dictionary."""
        data = {
            'id': self.id,
            'country_id': self.country_id,
            'name': self.name,
            'username': self.username,
            'birth_date': self.birth_date.isoformat() if self.birth_date is not None else None,
            'email': self.email,
            'email_verified_at': self.email_verified_at.isoformat() if self.email_verified_at is not None else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None,
        }

        return data
