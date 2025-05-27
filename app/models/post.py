from app.extensions import db
from app.enums.comment_enums import CommentableType
from app.enums.like_enums import LikeableType
from app.enums.save_enums import SaveableType 
from app.enums.media_enums import ModelType 
from datetime import datetime
from slugify import slugify
import ulid
import random

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    user_id = db.Column(db.CHAR(26), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50))
    slug = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship(
        'Comment',
        primaryjoin="and_(Comment.commentable_id == Post.id, Comment.commentable_type == '{}')".format(CommentableType.POST.value),
        foreign_keys='Comment.commentable_id',
    )
    likes = db.relationship(
        'Like',
        foreign_keys='Like.likeable_id',
        primaryjoin="and_(Post.id==Like.likeable_id, Like.likeable_type=='{}')".format(LikeableType.POST.value),
        overlaps="likeable_post"
    )
    saves = db.relationship(
        'Save',
        foreign_keys='Save.saveable_id',
        primaryjoin="and_(Post.id == Save.saveable_id, Save.saveable_type == '{}')".format(SaveableType.POST.value),
    )
    medias = db.relationship(
        'Media',
        foreign_keys='Media.model_id',
        primaryjoin="and_(Post.id == Media.model_id, Media.model_type == '{}')".format(ModelType.POST.value),
        overlaps="medias,model_user,avatar"
    )
    images = db.relationship(
        'Media',
        foreign_keys='Media.model_id',
        primaryjoin="and_(Post.id == Media.model_id, Media.model_type == '{}', Media.collection_name == 'post_images')".format(ModelType.POST.value),
        overlaps='medias,model_user,avatar',
        lazy='joined'
    )

    # ==========================================
    # Slug handling
    # ==========================================
    def generate_slug(self):
        slugable = self.title if self.title is not None else self.body
        self.slug = slugify(slugable)[:44] + '-' + str(random.randint(100000, 999999))

    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title if self.title else None,
            'slug': self.slug,
            'body': self.body,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        return data
