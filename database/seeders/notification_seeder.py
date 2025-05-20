from app.extensions import db
from app.models import Notification, User, Role
from database.seeders.seeder import Seeder
from app.enums.notification_enums import  Type as NotificationType, NotifiableType
from datetime import datetime
from faker import Faker

fake = Faker()

class NotificationSeeder(Seeder):

    def run(self):
        super().run()

        users = User.query.all()
        roles = Role.query.all()

        notifications = []
        
        for user in users:
            for _ in range(10):            
                created_at = fake.date_time_between(start_date='-1y', end_date='now')
                read_at = fake.date_time_between(start_date=created_at, end_date='now') if fake.boolean() else None
                title = ' '.join(fake.words(nb=2)) if fake.boolean() else None
                data = fake.json() if fake.boolean() else None

                notifications.append(Notification(
                    notifiable_id=user.id,
                    notifiable_type=NotifiableType.USER.value,
                    type=NotificationType.DEFAULT.value,
                    title=title,
                    message=fake.sentence(),
                    data=data,
                    read_at=read_at,
                    created_at=created_at,
                    updated_at=None
                ))

        for role in roles:
            for _ in range(5):            
                created_at = fake.date_time_between(start_date='-1y', end_date='now')
                read_at = fake.date_time_between(start_date=created_at, end_date='now') if fake.boolean() else None
                title = ' '.join(fake.words(nb=2)) if fake.boolean() else None
                data = fake.json() if fake.boolean() else None

                notifications.append(Notification(
                    notifiable_id=role.id,
                    notifiable_type=NotifiableType.ROLE.value,
                    type=NotificationType.DEFAULT.value,
                    title=title,
                    message=fake.sentence(),
                    data=data,
                    read_at=read_at,
                    created_at=created_at,
                    updated_at=None
                ))

        try:
            db.session.bulk_save_objects(notifications)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
