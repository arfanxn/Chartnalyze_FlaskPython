from app.repositories.repository import Repository
from app.extensions import mongo
from werkzeug.exceptions import NotFound, Conflict
from datetime import datetime 

class WatchedAssetRepository(Repository):

    def __init__(self):
        super().__init__()
    
    def all_by_user_id(self, user_id: str, keyword: str = None) -> tuple[list[object]]:
        """
        Get all watched assets for a given user ID.

        Args:
            user_id (str): The user ID to get watched assets for.
            keyword (str, optional): An optional keyword to search for in the name of the watched assets. Defaults to None.

        Returns:
            tuple[list[object]]: A tuple containing a list of watched asset objects, sorted by order.
        """
        find = {}
        find['user_id'] = user_id

        if keyword:
            regex_pattern = f".*{keyword}.*"
            find['name'] = {"$regex": regex_pattern, "$options": "i"}

        cursor = mongo.db.watched_assets.find(find).sort([('order', 1), ('created_at', -1)]).limit(100)
        watched_assets = list(cursor)
        return (watched_assets, )
    
    def store(self, asset: object) -> tuple[object, object]:
        existing_asset = mongo.db.watched_assets.find_one({
            'user_id': asset['user_id'],
            'key': asset['key']
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