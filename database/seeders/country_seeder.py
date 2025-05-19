from app.extensions import db
from app.models import Country
from database.seeders.seeder import Seeder
from datetime import date
import pycountry

class CountrySeeder(Seeder):

    def run(self):
        super().run()

        for c in pycountry.countries:
            country = Country()
            country.name = c.name
            country.iso_code = c.alpha_2
            db.session.add(country)

        db.session.commit()