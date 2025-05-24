from database.seeders.seeder import Seeder
from app.models import User
from app.extensions import mongo
from faker import Faker

fake = Faker()

class WatchedAssetSeeder(Seeder):

    def run(self):
        super().run()

        mongo.db.watched_assets.delete_many({})

        users = User.query.all()

        watched_assets = []

        for user in users:
            for i in range(fake.random_int(min=0, max=9, step=1)):
                symbol, name = fake.cryptocurrency()
                key = name.lower()
                image_url = fake.image_url(width=40, height=40)
                created_at = fake.date_time_between(start_date='-1y', end_date='now')
                created_at_iso_formatted = created_at.strftime("%Y-%m-%dT%H:%M:%S")
                updated_at = fake.date_time_between(start_date=created_at, end_date='now') if fake.boolean() else None
                updated_at_iso_formatted = updated_at.strftime("%Y-%m-%dT%H:%M:%S") if updated_at else None
                watched_assets.append({
                    'user_id': user.id,
                    'key': key,
                    'name': name,
                    'symbol': symbol,
                    'order' : i,
                    'image_url': image_url,
                    'created_at': created_at_iso_formatted,
                    'updated_at': updated_at_iso_formatted,
                })

        mongo.db.watched_assets.insert_many(watched_assets)

