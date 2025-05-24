from app.middlewares import api_key_verified
from app.services import WatchedAssetService
from app.forms import QueryForm, StoreWatchedAssetForm, UpdateWatchedAssetOrderForm
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, api_key_verified, email_verified
from app.resources import WatchedAssetResource
from flask import Blueprint, request
from http import HTTPStatus

wa_service = WatchedAssetService()

wa_bp = Blueprint('asset_watchlist', __name__)
watched_asset_bp = wa_bp

@wa_bp.route('/users/self/watched-assets', methods=['GET'])
@api_key_verified
@authenticated
@email_verified
def index():
    form = QueryForm(request.args)
    form.try_validate()
    
    watched_assets, = wa_service.all_watched_assets_by_self(form=form)
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
    
    watched_asset, = wa_service.store_by_self(form=form)
    watched_asset_json = WatchedAssetResource(watched_asset).to_json()
    
    return create_response_tuple(
        status=HTTPStatus.OK,
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
    
    asset, = wa_service.update_order_by_self(form=form)
    
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
    wa_service.destroy_by_self_and_watched_asset_key(watched_asset_key=watched_asset_key)
    
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Asset removed from watched assets successfully',
    )

