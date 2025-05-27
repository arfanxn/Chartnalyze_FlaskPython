from app.middlewares import api_key_verified, authenticated, email_verified
from app.resources import FollowResource
from app.services import FollowService 
from app.helpers.response_helpers import create_response_tuple
from flask import Blueprint, g
from http import HTTPStatus

follow_service = FollowService()

follow_bp = Blueprint('follow', __name__)

@follow_bp.route('/users/<string:followed_id>/followers', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def followers_index(followed_id: str):
    follows, meta = follow_service.paginate_followers_of(followed_id=followed_id)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Followers paginated successfully',
        data={'follows': FollowResource.collection(follows), **meta}
    )

@follow_bp.route('/users/<string:follower_id>/followeds', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def followeds_index(follower_id: str):
    follows, meta = follow_service.paginate_followeds_of(follower_id=follower_id)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Followeds paginated successfully',
        data={'follows': FollowResource.collection(follows), **meta}
    )

@follow_bp.route('/users/self/toggle-follow/<followed_id>', methods=['PATCH'])
@api_key_verified
@authenticated
@email_verified
def self_toggle_follow (followed_id: str):
    follower_id = g.user.id

    is_following, = follow_service.toggle_follow(follower_id=follower_id, followed_id=followed_id)

    message = 'Followed successfully' if is_following else 'Unfollowed successfully'

    return create_response_tuple(
        status=HTTPStatus.OK,
        message=message
    )
