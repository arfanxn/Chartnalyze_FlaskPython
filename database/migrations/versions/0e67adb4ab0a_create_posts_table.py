"""create_posts_table

Revision ID: 0e67adb4ab0a
Revises: 8cd29dc7ba4f
Create Date: 2025-05-19 09:55:41.230723

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e67adb4ab0a'
down_revision = '8cd29dc7ba4f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('user_id', sa.CHAR(26), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.VARCHAR(50), nullable=False),
        sa.Column('slug', sa.VARCHAR(50), nullable=False),
        sa.Column('body', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now())
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass