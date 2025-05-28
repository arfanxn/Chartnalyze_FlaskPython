from app.middlewares import api_key_verified
from app.services import WatchedAssetService
from app.forms import StoreWatchedAssetForm, UpdateWatchedAssetOrderForm
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, api_key_verified, email_verified
from app.resources import WatchedAssetResource
from flask import Blueprint, request, g
from http import HTTPStatus

wa_service = WatchedAssetService()

wa_bp = Blueprint('asset_watchlist', __name__)
watched_asset_bp = wa_bp

@wa_bp.route('/users/self/watched-assets', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index():
    user_id = g.user.id
    
    watched_assets, = wa_service.all(user_id=user_id)
    watched_assets_json = WatchedAssetResource.collection(watched_assets)
    
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Watched assets retrieved successfully',
        data={'watched_assets': watched_assets_json},
    )


@wa_bp.route('/users/self/watched-assets', methods=['POST'])
@api_key_verified
@authenticated
@email_verified
def store (): 
    form = StoreWatchedAssetForm(request.form)
    form.try_validate()

    user_id = g.user.id
    
    watched_asset, = wa_service.store(form=form, user_id=user_id)
    watched_asset_json = WatchedAssetResource(watched_asset).to_json()
    
    return create_response_tuple(
        status=HTTPStatus.CREATED,
        message='Asset stored into watched assets successfully',
        data={'watched_asset': watched_asset_json},
    )

@wa_bp.route('/users/self/watched-assets/<string:watched_asset_key>/order', methods=['PATCH'])
@api_key_verified
@authenticated
@email_verified
def update_order (watched_asset_key: str): 
    form = UpdateWatchedAssetOrderForm(request.form)
    form.key.data = watched_asset_key
    form.try_validate()

    user_id = g.user.id
    
    asset, = wa_service.update_order(form=form, user_id=user_id)
    
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Asset order updated successfully',
        data={'watched_asset': asset}
    )


@wa_bp.route('/users/self/watched-assets/<string:watched_asset_key>', methods=['DELETE'])
@api_key_verified
@authenticated
@email_verified
def destroy (watched_asset_key: str): 
    user_id = g.user.id 

    wa_service.destroy(watched_asset_key=watched_asset_key, user_id=user_id)
    
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Asset removed from watched assets successfully',
    )

