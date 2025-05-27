from app.extensions import db
from app.enums.media_enums import ModelType
from datetime import datetime
import ulid

class Media(db.Model):
    __tablename__ = 'medias'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    model_id = db.Column(db.CHAR(26), nullable=False)
    model_type = db.Column(db.Enum(*[e.value for e in ModelType], name='model_types'), nullable=False)
    collection_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(50), nullable=False)
    disk = db.Column(db.String(50))
    size = db.Column(db.BigInteger, nullable=False)
    data = db.Column(db.JSON)
    order = db.Column(db.Integer) # order in collection
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    model_user = db.relationship(
        'User',
        foreign_keys='Media.model_id',
        primaryjoin="and_(Media.model_id == User.id, Media.model_type == '{}')".format(ModelType.USER.value),
        back_populates='medias',
        overlaps='model_post,medias,avatar,images'
    )
    model_post = db.relationship(
        'Post',
        foreign_keys='Media.model_id',
        primaryjoin="and_(Media.model_id == Post.id, Media.model_type == '{}')".format(ModelType.POST.value),
        back_populates='medias',
        overlaps='model_user,medias,avatar,images'
    )
    @property   
    def model(self):
        if self.model_type == ModelType.USER.value:
            return self.model_user
        elif self.model_type == ModelType.POST.value:
            return self.model_post
        else: 
            return None


    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        data = {
            'id': self.id,
            'model_id': self.model_id,
            'model_type': self.model_type,
            'collection_name': self.collection_name,
            'name': self.name,
            'file_name': self.file_name,
            'mime_type': self.mime_type,
            'disk': self.disk,
            'size': self.size,
            'data': self.data,
            'order': self.order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        return data
