from app.services import Service
from app.repositories import WatchedAssetRepository
from app.forms import StoreWatchedAssetForm, UpdateWatchedAssetOrderForm
from flask import g

wa_repository = WatchedAssetRepository()

class WatchedAssetService(Service):

    def __init__(self):
        super().__init__()
    
    def all (self, user_id: str|None = None) -> tuple[list[object]]:
        watched_assets, = wa_repository.all(user_id=user_id)
        return (watched_assets, )
    
    def store(self, form: StoreWatchedAssetForm, user_id: str) -> tuple[object]:
        watched_asset = {
            'user_id': user_id,
            'key': form.key.data,
            'name': form.name.data,
            'symbol': form.symbol.data,
            'order' : form.order.data,
            'image_url': form.image_url.data,
        }

        watched_asset, _ = wa_repository.store(asset=watched_asset)

        return (watched_asset, )
    
    def update_order(self, form: UpdateWatchedAssetOrderForm, user_id: str) -> tuple[object, bool]:
        asset, _ = wa_repository.\
            update_order_by_user_id_and_key(
                user_id=user_id,
                watched_asset_key=form.key.data,
                order=form.order.data
            )

        return (asset, )
    
    def destroy(self, watched_asset_key: str, user_id: str) -> tuple[bool]:        
        wa_repository.\
            destroy_by_user_id_and_key(
                user_id=user_id,
                watched_asset_key=watched_asset_key
            )

        return (True, )