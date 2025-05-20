from app.extensions import db
from app.enums.save_enums import SaveableType
from datetime import datetime
import ulid

class Save(db.Model):
    __tablename__ = 'saves'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    user_id = db.Column(db.CHAR(26), db.ForeignKey('users.id'), nullable=False)
    saveable_id = db.Column(db.CHAR(26), nullable=False)
    saveable_type = db.Column(db.Enum(*[e.value for e in SaveableType], name='saveable_types'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    user = db.relationship('User', back_populates='saves')
    saveable_post = db.relationship(
        'Post',
        foreign_keys='Save.saveable_id',
        primaryjoin="and_(Save.saveable_id == Post.id, Save.saveable_type == '{}')".format(SaveableType.POST.value),
        back_populates='saves',
        # overlaps="" # * Now is not needed unless we add another polymorphic relation
    )
    @property   
    def saveable(self):
        if self.saveable_type == SaveableType.POST.value:
            return self.saveable_post
        else: 
            return None


    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'saveable_id': self.saveable_id,
            'saveable_type': self.saveable_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        return data
