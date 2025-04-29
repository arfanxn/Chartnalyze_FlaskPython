from app.extensions import db

class PermissionRole(db.Model):
    __tablename__ = 'permission_role'

    permission_id = db.Column(
        db.CHAR(26), 
        db.ForeignKey('permissions.id'), 
        primary_key=True
    )
    role_id = db.Column(
        db.CHAR(26), 
        db.ForeignKey('roles.id'), 
        primary_key=True
    )