from app.extensions import db
from app.enums.like_enums import LikeableType
from datetime import datetime
import ulid

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    user_id = db.Column(db.CHAR(26), db.ForeignKey('users.id'), nullable=False)
    likeable_id = db.Column(db.CHAR(26), nullable=False)
    likeable_type = db.Column(db.Enum(*[e.value for e in LikeableType], name='likeable_types'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    user = db.relationship('User', back_populates='likes')

    likeable_post = db.relationship(
        'Post',
        foreign_keys='Like.likeable_id',
        primaryjoin="and_(Like.likeable_id == Post.id, Like.likeable_type == '{}')".format(LikeableType.POST.value),
        viewonly=True,
        overlaps="likes"
    )
    likeable_comment = db.relationship(
        'Comment',
        foreign_keys='Like.likeable_id',
        primaryjoin="and_(Like.likeable_id == Comment.id, Like.likeable_type == '{}')".format(LikeableType.COMMENT.value),
        back_populates='likes',
        overlaps="likes"
    )
    @property   
    def likeable(self):
        if self.likeable_type == LikeableType.POST.value:
            return self.likeable_post
        elif self.likeable_type == LikeableType.COMMENT.value:
            return self.likeable_comment
        else: 
            return None


    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'likeable_id': self.likeable_id,
            'likeable_type': self.likeable_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        return data
