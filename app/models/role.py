from app.extensions import db
from app.enums.notification_enums import NotifiableType
from datetime import datetime
import ulid

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    users = db.relationship(
        'User', 
        secondary='role_user', 
        back_populates='roles'
    )
    permissions = db.relationship(
        'Permission', 
        secondary='permission_role', 
        back_populates='roles'
    )
    notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.notifiable_id",
        primaryjoin="and_(Role.id == Notification.notifiable_id,Notification.notifiable_type == '{}')".format(NotifiableType.ROLE.value),
        back_populates="notifiable_role",
        overlaps="notifiable_user,notifications"
    )

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
