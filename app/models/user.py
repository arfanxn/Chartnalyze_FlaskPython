from app.extensions import db
from datetime import datetime
import bcrypt
import ulid

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.CHAR(26), primary_key=True, default=lambda: ulid.new().str)
    name = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(16), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.password = hashed_password

    def check_password(self, password):
        isMatch =  bcrypt.checkpw(password=password, hashed_password= self.password)
        print('PASSWORD IS MATCH', isMatch)
        return bcrypt.checkpw(password=password, hashed_password= self.password)


    def __repr__(self):
        return f"<User {self.name}>"
