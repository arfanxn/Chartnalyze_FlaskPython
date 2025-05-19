"""create_saves_table

Revision ID: e9111394ed36
Revises: 4c3237406d60
Create Date: 2025-05-19 10:06:31.996852

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e9111394ed36'
down_revision = '4c3237406d60'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('saves',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('user_id', sa.CHAR(26), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('saveable_id', sa.CHAR(26), sa.ForeignKey('posts.id'), nullable=False),
        sa.Column('saveable_type', sa.Enum('post', name='saveable_type'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now())
    )
    pass


def downgrade():
    op.drop_table('saves')
    pass