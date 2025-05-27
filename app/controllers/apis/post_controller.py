from app.middlewares import api_key_verified
from app.services import PostService
from app.forms import SavePostForm
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, api_key_verified, email_verified
from app.resources import PostResource
from flask import Blueprint, request
from http import HTTPStatus

post_service = PostService()

post_bp = Blueprint('post', __name__)

@post_bp.route('/posts', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index():    
    posts, meta = post_service.paginate()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Posts paginated successfully',
        data={'posts': PostResource.collection(posts), **meta}
    )

@post_bp.route('/users/<string:user_id>/posts', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index_by_user(user_id: str):
    posts, meta = post_service.paginate_by_user(user_id=user_id)
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Posts paginated successfully', 
        data={'posts': PostResource.collection(posts), **meta}
    )

@post_bp.route('/posts/<string:post_id>', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def show(post_id: str):
    post, = post_service.show(post_id=post_id)
    post_json = PostResource(post).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Post found successfully',
        data={'post': post_json}
    )

@post_bp.route('/posts', methods=['POST'])
@api_key_verified
@authenticated
@email_verified
def store():
    form = SavePostForm(request.form)
    form.try_validate()

    images = request.files.getlist('images')

    post, = post_service.store(form=form, images=images)
    post_json = PostResource(post).to_json()

    return create_response_tuple(
        status=HTTPStatus.CREATED,
        message='Post created successfully',
        data={'post': post_json}
    )

@post_bp.route('/posts/<string:post_id>', methods=['PUT'])
@api_key_verified
@authenticated
@email_verified
def update(post_id: str):
    form = SavePostForm(request.form)
    form.try_validate()

    post, = post_service.update(form=form, post_id=post_id)
    post_json = PostResource(post).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Post updated successfully',
        data={'post': post_json}
    )

@post_bp.route('/posts/<string:post_id>', methods=['DELETE'])
@api_key_verified
@authenticated
@email_verified
def destroy(post_id: str):
    post_service.destroy(post_id=post_id)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Post deleted successfully'
    )