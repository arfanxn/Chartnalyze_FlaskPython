from app.extensions import db

class RoleUser(db.Model):
    __tablename__ = 'role_user'

    role_id = db.Column(
        db.CHAR(26), 
        db.ForeignKey('roles.id'),  # Add foreign key
        primary_key=True  # Composite primary key
    )
    user_id = db.Column(
        db.CHAR(26), 
        db.ForeignKey('users.id'),  # Add foreign key
        primary_key=True  # Composite primary key
    )