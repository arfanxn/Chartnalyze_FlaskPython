from app.extensions import db
from app.enums.activity_enums import SubjectType, Type
from datetime import datetime
import ulid

class Activity(db.Model):
    __tablename__ = 'activities'

    # ==========================================
    # Columns Definition
    # ==========================================
    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    user_id = db.Column(db.CHAR(26), db.ForeignKey('users.id'), nullable=False)
    user_ip_address = db.Column(db.VARCHAR(45), nullable=False)
    user_agent = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(*[e.value for e in Type], name='types'), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.CHAR(26))
    subject_type = db.Column(db.Enum(*[e.value for e in SubjectType], name='subject_types'))
    properties = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    user = db.relationship('User', back_populates='activities')

    subject_user = db.relationship(
        'User',
        foreign_keys='Activity.subject_id',
        primaryjoin="and_(Activity.subject_id == User.id, Activity.subject_type == '{}')".format(SubjectType.USER.value),
        # overlaps="" # * Now is not needed unless we add another polymorphic relation
    )
    @property   
    def subject(self):
        if self.subject_type == SubjectType.USER.value:
            return self.subject_user
        else: 
            return None

    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'user_ip_address': self.user_ip_address,
            'user_agent': self.user_agent,
            'type': self.type.value,
            'description': self.description,
            'subject_id': self.subject_id,
            'subject_type': self.subject_type.value,
            'properties': self.properties,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        return data
