from database.seeders.country_seeder import CountrySeeder
from database.seeders.permission_seeder import PermissionSeeder
from database.seeders.role_seeder import RoleSeeder
from database.seeders.user_seeder import UserSeeder
from database.seeders.notification_seeder import NotificationSeeder
from database.seeders.follow_seeder import FollowSeeder
from database.seeders.post_seeder import PostSeeder 
from database.seeders.comment_seeder import CommentSeeder 
from database.seeders.like_seeder import LikeSeeder
from database.seeders.save_seeder import SaveSeeder
from database.seeders.watched_asset_seeder import WatchedAssetSeeder
from database.seeders.seeder import Seeder

_registered_seeders: list[Seeder] = [
    CountrySeeder(),
    PermissionSeeder(),
    RoleSeeder(),
    UserSeeder(),
    NotificationSeeder(),
    FollowSeeder(),
    PostSeeder(),
    CommentSeeder(),
    LikeSeeder(),
    SaveSeeder(),
    WatchedAssetSeeder(),
]

def run_registered_seeders ():
    for seeder in _registered_seeders:
        seeder.run()