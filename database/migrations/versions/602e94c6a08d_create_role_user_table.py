"""create role_user table

Revision ID: 602e94c6a08d
Revises: e87586e228aa
Create Date: 2025-04-29 14:55:10.468631

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '602e94c6a08d'
down_revision = 'e87586e228aa'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('role_user',
        sa.Column('role_id', sa.CHAR(length=26), sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('user_id', sa.CHAR(length=26), sa.ForeignKey('users.id'), nullable=False),
    )

def downgrade():
    op.drop_table('role_user')   