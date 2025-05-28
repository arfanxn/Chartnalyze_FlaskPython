from app.repositories.repository import Repository
from app.extensions import mongo
from flask import request
from werkzeug.exceptions import NotFound, Conflict
from datetime import datetime 

class WatchedAssetRepository(Repository):

    def __init__(self):
        super().__init__()
    
    def all(self, user_id: str|None = None) -> tuple[list[object]]:
        filter = request.args.get('filter', None)

        find = {}
        if user_id is not None:
            find['user_id'] = user_id

        if filter is not None:
            regex_pattern = f".*{filter}.*"
            find['name'] = {"$regex": regex_pattern, "$options": "i"}

        cursor = mongo.db.watched_assets.find(find).sort([('order', 1), ('created_at', -1)]).limit(10)
        watched_assets = list(cursor)
        return (watched_assets, )
    
    def store(self, asset: object) -> tuple[object, object]:
        user_id, key = asset['user_id'], asset['key']

        count = mongo.db.watched_assets.count_documents({'user_id': user_id})
        if count >= 10:
            raise Conflict("Maximum 10 watched assets allowed per user")

        existing_asset = mongo.db.watched_assets.find_one({
            'user_id': user_id,
            'key': key
        })
        if existing_asset:
            raise Conflict(f"Asset already exists")
        
        asset.setdefault('order', 0)
        asset.setdefault('created_at', datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        result = mongo.db.watched_assets.insert_one(asset)
        asset.setdefault('_id', result.inserted_id)

        return (asset, result)
    
    def update_order_by_user_id_and_key(self, user_id: str, watched_asset_key: str, order: int) -> tuple[object, object]:
        asset = mongo.db.watched_assets.find_one({
            'user_id': user_id,
            'key': watched_asset_key
        })
        if not asset:
            raise NotFound(f'Watched asset not found')
        
        result = mongo.db.watched_assets.update_one(
            {'user_id': user_id, 'key': watched_asset_key},
            {'$set': {'order': order, 'updated_at':  datetime.now().strftime("%Y-%m-%dT%H:%M:%S")},}
        )
        asset['order'] = order
        return (asset, result)

    def destroy_by_user_id_and_key\
        (self, user_id: str, watched_asset_key: str) -> tuple[bool, object]:
        result = mongo.db.watched_assets.delete_one({
            'user_id': user_id,
            'key': watched_asset_key
        })
        if result.deleted_count == 0:
            raise NotFound(f'Watched asset not found')
        return (True, result)