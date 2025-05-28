from app.policies import CommentPolicy
from app.repositories import CommentRepository
from app.services import Service
from app.forms import StoreCommentForm
from app.models import Comment
from app.extensions import db
from flask import g 
from werkzeug.exceptions import NotFound, Forbidden
import ulid
import os

comment_policy = CommentPolicy()
comment_repository = CommentRepository()

class CommentService(Service):

    def __init__(self):
        super().__init__()
    
    def paginate (self, user_id: str|None = None, commentable_id: str|None = None) -> tuple[list[Comment], dict]:
        comments, meta = comment_repository.paginate(user_id=user_id, commentable_id=commentable_id)
        return (comments, meta)
    
    def show(self, comment_id: str) -> tuple[Comment]:
        comment, = comment_repository.show(comment_id=comment_id)
        if comment is None:
            raise NotFound('Comment not found')
        return (comment, )
    
    def store(
            self, 
            form: StoreCommentForm, 
            user_id:str, 
            commentable_id : str, 
            commentable_type: str
        ) -> tuple[Comment]:
        if form.parent_id.data is not None:
            parent_comment, = comment_repository.show(comment_id=form.parent_id.data)
            if parent_comment is None:
                raise NotFound('Parent comment not found')

        comment, = comment_repository.store(form=form, user_id=user_id, commentable_id=commentable_id, commentable_type=commentable_type)
        db.session.commit()
        return (comment, )
    
    def destroy (self, comment_id: str) -> tuple[bool]:
        comment,  = comment_repository.show(comment_id=comment_id)
        if comment is None:
            raise NotFound('Comment not found')
        
        if not comment_policy.destroy(g.user, comment):
            raise Forbidden('You are not allowed to delete this comment')

        comment_repository.destroy(comment=comment)
        db.session.commit()
        return (True, )