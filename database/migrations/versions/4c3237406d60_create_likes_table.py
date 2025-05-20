"""create_likes_table

Revision ID: 4c3237406d60
Revises: 0e67adb4ab0a
Create Date: 2025-05-19 10:01:14.437129

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from app.enums.like_enums import LikeableType

# revision identifiers, used by Alembic.
revision = '4c3237406d60'
down_revision = '0e67adb4ab0a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('likes',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('user_id', sa.CHAR(26), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('likeable_id', sa.CHAR(26), nullable=False),
        sa.Column('likeable_type', sa.Enum(*[e.value for e in LikeableType], name='likeable_types'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now())
    )
    pass


def downgrade():
    op.drop_table('likes')
    pass