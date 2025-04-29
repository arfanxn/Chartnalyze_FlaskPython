from app.extensions import db

class RoleUser(db.Model):
    __tablename__ = 'role_user'

    role_id = db.Column(db.CHAR(26), nullable=False)
    user_id = db.Column(db.CHAR(26), nullable=False)
