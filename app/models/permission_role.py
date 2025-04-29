from app.extensions import db

class PermissionRole(db.Model):
    __tablename__ = 'permission_role'

    permission_id = db.Column(db.CHAR(26), nullable=False)
    role_id = db.Column(db.CHAR(26), nullable=False)
