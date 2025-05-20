from app.extensions import db
from app.enums.notification_enums import NotifiableType
from datetime import datetime
import ulid

class Notification(db.Model):
    __tablename__ = 'notifications'

    # ==========================================
    # Columns Definition
    # ==========================================
    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    notifiable_id = db.Column(db.CHAR(26), nullable=False)
    notifiable_type = db.Column(db.Enum(*[e.value for e in NotifiableType], name='notifiable_types'), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50))
    message = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    notifiable_user = db.relationship(
        'User',
        foreign_keys='Notification.notifiable_id',
        primaryjoin="and_(Notification.notifiable_id == User.id, Notification.notifiable_type == '{}')".format(NotifiableType.USER.value),
        back_populates='notifications',
        overlaps="notifications,notifiable_role"
    )
    notifiable_role = db.relationship(
        'Role',
        foreign_keys='Notification.notifiable_id',
        primaryjoin="and_(Notification.notifiable_id == Role.id, Notification.notifiable_type == '{}')".format(NotifiableType.ROLE.value),
        back_populates='notifications',
        overlaps="notifications,notifiable_user"
    )
    @property   
    def notifiable(self):
        if self.notifiable_type == NotifiableType.USER.value:
            return self.notifiable_user
        elif self.notifiable_type == NotifiableType.ROLE.value:
            return self.notifiable_role
        else: 
            return None

    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        data = {
            'id': self.id,
            'notifiable_id': self.notifiable_id,
            'notifiable_type': self.notifiable_type,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'data': self.data,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        return data
