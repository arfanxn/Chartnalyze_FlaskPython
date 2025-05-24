from app.services import Service
from app.repositories import WatchedAssetRepository
from app.forms import StoreWatchedAssetForm, UpdateWatchedAssetOrderForm
from app.forms import QueryForm
from flask import g

wa_repository = WatchedAssetRepository()

class WatchedAssetService(Service):

    def __init__(self):
        super().__init__()
    
    def all_watched_assets_by_self (self, form: QueryForm) -> tuple[list[object]]:
        user_id = g.user.id

        watched_assets, = wa_repository.all_by_user_id(user_id=user_id, keyword=form.keyword.data)

        return (watched_assets, )
    
    def store_by_self(self, form: StoreWatchedAssetForm) -> tuple[object]:
        watched_asset = {
            'user_id': g.user.id,
            'key': form.key.data,
            'name': form.name.data,
            'symbol': form.symbol.data,
            'order' : form.order.data,
            'image_url': form.image_url.data,
        }

        watched_asset, _ = wa_repository.store(asset=watched_asset)

        return (watched_asset, )
    
    def update_order_by_self(self, form: UpdateWatchedAssetOrderForm) -> tuple[object, bool]:
        asset, _ = wa_repository.\
            update_order_by_user_id_and_key(
                user_id=g.user.id,
                watched_asset_key=form.key.data,
                order=form.order.data
            )

        return (asset, )
    
    def destroy_by_self_and_key(self, watched_asset_key: str) -> tuple[bool]:        
        user_id = g.user.id

        wa_repository.\
            destroy_by_user_id_and_key(
                user_id=user_id,
                watched_asset_key=watched_asset_key
            )

        return (True, )