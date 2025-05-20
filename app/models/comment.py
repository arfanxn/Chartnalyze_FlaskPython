from app.extensions import db
from app.enums.comment_enums import CommentableType
from app.enums.like_enums import LikeableType
from datetime import datetime
import ulid

class Comment(db.Model):
    __tablename__ = 'comments'

    # ==========================================
    # Columns Definition
    # ==========================================
    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    user_id = db.Column(db.CHAR(26), db.ForeignKey('users.id'), nullable=False)
    commentable_id = db.Column(db.CHAR(26), nullable=False)
    commentable_type = db.Column(db.Enum(*[e.value for e in CommentableType], name='commentable_types'), nullable=False)
    parent_id = db.Column(db.CHAR(26), db.ForeignKey('comments.id'), nullable=True)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now())

    # ==========================================
    # Relationships
    # ==========================================
    user = db.relationship('User', back_populates='comments')
    commentable_post = db.relationship(
        'Post',
        foreign_keys='Comment.commentable_id',
        primaryjoin="and_(Comment.commentable_id == Post.id, Comment.commentable_type == '{}')".format(CommentableType.POST.value),
        back_populates='comments',
        # overlaps="" # * Now is not needed unless we add another polymorphic relation
    )
    @property   
    def commentable(self):
        if self.commentable_type == CommentableType.POST.value:
            return self.commentable_post
        else: 
            return None
    parent = db.relationship('Comment', remote_side=[id], back_populates='children')
    children = db.relationship('Comment', remote_side=[parent_id], back_populates='parent')
    likes = db.relationship(
        'Like',
        foreign_keys="Like.likeable_id",
        primaryjoin="and_(Comment.id == Like.likeable_id, Like.likeable_type == '{}')".format(LikeableType.COMMENT.value),
        viewonly=True,
        overlaps="likeable_comment"
    )


    # ==========================================
    # Serialization to JSON
    # ==========================================
    def to_json(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'commentable_id': self.commentable_id,
            'commentable_type': self.commentable_type,
            'parent_id': self.parent_id if self.parent_id else None,
            'body': self.body,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        return data
