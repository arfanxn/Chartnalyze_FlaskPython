from app.middlewares import api_key_verified, authenticated, authorized, email_verified
from app.resources import UserResource
from app.services import FollowService 
from app.extensions import limiter
from app.forms import QueryForm
from app.helpers.response_helpers import create_response_tuple
from flask import Blueprint, request, g
from http import HTTPStatus

follow_service = FollowService()

follow_bp = Blueprint('follow', __name__)

@follow_bp.route('/users/<string:user_id>/followers', methods=['GET'])
@api_key_verified
@authenticated
@authenticated
@email_verified
def followers_index(user_id: str):
    form = QueryForm(request.args)
    form.try_validate()

    users, meta = follow_service.followers_index(form=form, user_id=user_id)
    users_json = UserResource.collection(users)
    users_pagination = {'users': users_json, **meta}

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Followers paginated successfully',
        data={ **users_pagination }
    )


@follow_bp.route('/users/<string:user_id>/followeds', methods=['GET'])
@api_key_verified
@authenticated
@authenticated
@email_verified
def followeds_index(user_id: str):
    form = QueryForm(request.args)
    form.try_validate()

    users, meta = follow_service.followeds_index(form=form, user_id=user_id)
    users_json = UserResource.collection(users)
    users_pagination = {'users': users_json, **meta}

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Followeds paginated successfully',
        data={ **users_pagination }
    )

@follow_bp.route('/users/self/toggle-follow/<followed_id>', methods=['PATCH'])
@api_key_verified
@authenticated
@authenticated
@email_verified
def self_toggle_follow (followed_id: str):
    follower_id = g.user.id

    is_following = follow_service.toggle_follow(follower_id=follower_id, followed_id=followed_id)

    message = 'Followed successfully' if is_following else 'Unfollowed successfully'

    return create_response_tuple(
        status=HTTPStatus.OK,
        message=message
    )
