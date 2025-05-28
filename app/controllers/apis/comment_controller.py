from app.enums.comment_enums import CommentableType 
from app.middlewares import api_key_verified
from app.services import CommentService
from app.forms import StoreCommentForm
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, api_key_verified, email_verified
from app.resources import CommentResource
from flask import Blueprint, request, g
from http import HTTPStatus

comment_service = CommentService()

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/posts/<string:post_id>/comments', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index_by_post(post_id: str):
    comments, meta = comment_service.paginate(commentable_id=post_id)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Comments paginated successfully',
        data={'comments': CommentResource.collection(comments), **meta}
    )

@comment_bp.route('/users/<string:user_id>/comments', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index_by_user(user_id: str):
    comments, meta = comment_service.paginate(user_id=user_id)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Comments paginated successfully',
        data={'comments': CommentResource.collection(comments), **meta}
    )

@comment_bp.route('/comments/<string:comment_id>', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def show(comment_id: str):
    comment, = comment_service.show(comment_id=comment_id)
    comment_json = CommentResource(comment).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Comment found successfully',
        data={'comment': comment_json}
    )

@comment_bp.route('/posts/<string:post_id>/comments', methods=['POST'])
@api_key_verified
@authenticated
@email_verified
def store(post_id: str):
    form = StoreCommentForm(request.form)
    form.try_validate()

    user_id = g.user.id

    comment, = comment_service.store(
        form=form, 
        user_id=user_id, 
        commentable_id=post_id, 
        commentable_type=CommentableType.POST.value
    )
    comment_json = CommentResource(comment).to_json()

    return create_response_tuple(
        status=HTTPStatus.CREATED,
        message='Comment created successfully',
        data={'comment': comment_json}
    )

@comment_bp.route('/comments/<string:comment_id>', methods=['DELETE'])
@api_key_verified
@authenticated
@email_verified
def destroy(comment_id: str):
    comment_service.destroy(comment_id=comment_id)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Comment deleted successfully'
    )