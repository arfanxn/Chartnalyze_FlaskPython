from app.enums.like_enums import LikeableType 
from app.services import LikeService
from app.resources import LikeResource
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, api_key_verified, email_verified
from flask import Blueprint, g
from http import HTTPStatus

like_service = LikeService()

like_bp = Blueprint('like', __name__)

@like_bp.route('/posts/<string:post_id>/likes', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index_by_post(post_id: str):
    likes, meta = like_service.paginate(likeable_id=post_id, likeable_type=LikeableType.POST.value)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Likes paginated successfully',
        data={'likes': LikeResource.collection(likes), **meta}
    )

@like_bp.route('/comments/<string:comment_id>/likes', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index_by_comment(comment_id: str):
    likes, meta = like_service.paginate(likeable_id=comment_id, likeable_type=LikeableType.COMMENT.value)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Likes paginated successfully',
        data={'likes': LikeResource.collection(likes), **meta}
    )

@like_bp.route('/users/<string:user_id>/likes', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index_by_user(user_id: str):
    likes, meta = like_service.paginate(user_id=user_id)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Likes paginated successfully',
        data={'likes': LikeResource.collection(likes), **meta}
    )

@like_bp.route('/likes/<string:like_id>', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def show(like_id: str):
    like, = like_service.show(like_id=like_id)
    like_json = LikeResource(like).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Like found successfully',
        data={'like': like_json}
    )

@like_bp.route('/posts/<string:post_id>/toggle-like', methods=['PATCH'])
@api_key_verified
@authenticated
@email_verified
def toggle_like_post (post_id: str):
    user_id = g.user.id

    is_liked, = like_service.toggle(
        user_id=user_id, 
        likeable_id=post_id, 
        likeable_type=LikeableType.POST.value
    )

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Post is liked' if is_liked else 'Post is unliked',
    )

@like_bp.route('/comments/<string:comment_id>/toggle-like', methods=['PATCH'])
@api_key_verified
@authenticated
@email_verified
def toggle_like_comment (comment_id: str):
    user_id = g.user.id

    is_liked, = like_service.toggle(
        user_id=user_id, 
        likeable_id=comment_id, 
        likeable_type=LikeableType.COMMENT.value
    )

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Commend is liked' if is_liked else 'Comment is unliked',
    )