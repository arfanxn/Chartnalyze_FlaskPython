from app.extensions import db
from app.models import User, Activity
from app.enums.activity_enums import Type
from database.seeders.seeder import Seeder
from faker import Faker

fake = Faker()

class ActivitySeeder(Seeder):

    def run(self):
        """
        Seeds activity records for users, including registration, email verification,
        login, and logout activities.

        For each user, generates:
        - A registration activity with properties containing user details.
        - An optional email verification activity if the user's email has been verified.
        - A series of login activities, with random timestamps.
        - A series of logout activities following each login, with random timestamps.

        All generated activities are saved to the database. If an error occurs during
        the commit, the transaction is rolled back and the error is re-raised.
        """

        super().run()

        # Fetch all users from the database
        users = User.query.all()

        # List to store generated activity objects
        activities = []

        # Loop through each user to generate activity records
        for user in users:
            ip_address = fake.ipv4(),
            user_agent = fake.user_agent(),

            # Create registration activity
            activity = Activity(
                user_ip_address=ip_address,
                user_agent=user_agent,
                user_id=user.id,
                type=Type.REGISTER.value,
                description=f"{user.name} ({user.email}) has registered",
                created_at=user.created_at.isoformat(),
                updated_at=None
            )
            activities.append(activity)

            # Create email verification activity if applicable
            if user.email_verified_at is not None:

                activity = Activity(
                    user_id=user.id,
                    user_ip_address=ip_address,
                    user_agent=user_agent,
                    type=Type.VERIFY_EMAIL.value,
                    description=f"{user.name} ({user.email}) has verified their email",
                    created_at=user.email_verified_at.isoformat(),
                    updated_at=None
                )
                activities.append(activity)

            # Generate login and logout activities
            login_count = range(fake.random_int(
                min=1 if user.email_verified_at is not None else 0,
                max=5,
                step=1
            ))
            for i in login_count:
                # Randomly generate login timestamp
                logged_in_at = fake.date_time_between(start_date=user.created_at, end_date="now")

                # Create login activity
                activity = Activity(
                    user_id=user.id,
                    user_ip_address=ip_address,
                    user_agent=user_agent,
                    type=Type.LOGIN.value,
                    description=f"{user.name} ({user.email}) has logged in",
                    created_at=logged_in_at.isoformat(),
                    updated_at=None
                )
                activities.append(activity)

                # Determine if a logout activity should be created
                if i == len(login_count) - 1 and not fake.boolean():
                    continue

                # Randomly generate logout timestamp after login
                logged_out_at = fake.date_time_between(start_date=logged_in_at, end_date="now")

                # Create logout activity
                activity = Activity(
                    user_id=user.id,
                    user_ip_address=ip_address,
                    user_agent=user_agent,
                    type=Type.LOGOUT.value,
                    description=f"{user.name} ({user.email}) has logged out",
                    created_at=logged_out_at.isoformat(),
                    updated_at=None
                )
                activities.append(activity)

        # Attempt to save all generated activities to the database
        try:
            db.session.bulk_save_objects(activities)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


