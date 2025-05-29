from app.middlewares import api_key_verified
from app.services import SaveService
from app.enums.save_enums import SaveableType
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, api_key_verified, email_verified
from app.resources import SaveResource
from flask import Blueprint, g
from http import HTTPStatus

save_service = SaveService()

save_bp = Blueprint('save', __name__)

@save_bp.route('/users/self/saved_posts', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def saved_posts_by_self():
    user_id = g.user.id
    saves, meta = save_service.paginate(user_id=user_id, saveable_type=SaveableType.POST.value)
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Saved posts paginated successfully', 
        data={'saved_posts': SaveResource.collection(saves), **meta}
    )

@save_bp.route('/saves/<string:save_id>', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def show(save_id): 
    save, = save_service.show(save_id=save_id)
    save_json = SaveResource(save).to_json()

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Save found successfully',
        data={'save': save_json}
    )

@save_bp.route('/posts/<string:post_id>/toggle-save', methods=['PATCH'])
@api_key_verified
@authenticated
@email_verified
def toggle_save_post (post_id: str):
    user_id = g.user.id

    is_saved, = save_service.toggle(
        user_id=user_id, 
        saveable_id=post_id, 
        saveable_type=SaveableType.POST.value
    )

    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Entity is saved' if is_saved else 'Entity is unsaved',
    )