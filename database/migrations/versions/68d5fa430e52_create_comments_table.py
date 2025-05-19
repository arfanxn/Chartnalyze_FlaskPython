"""create_comments_table

Revision ID: 68d5fa430e52
Revises: e9111394ed36
Create Date: 2025-05-19 10:08:51.617401

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '68d5fa430e52'
down_revision = 'e9111394ed36'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('comments',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('user_id', sa.CHAR(26), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('commentable_id', sa.CHAR(26), sa.ForeignKey('posts.id'), nullable=False),
        sa.Column('commentable_type', sa.Enum('post', name='commentable_type'), nullable=False),
        sa.Column('parent_id', sa.CHAR(26), sa.ForeignKey('comments.id'), nullable=True),
        sa.Column('body', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now())
    )
    pass


def downgrade():
    op.drop_table('comments')
    pass