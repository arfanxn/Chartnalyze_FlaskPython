"""create_follows_table

Revision ID: 8cd29dc7ba4f
Revises: aa5046bad359
Create Date: 2025-05-19 09:41:37.337161

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8cd29dc7ba4f'
down_revision = 'aa5046bad359'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('follows',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('follower_id', sa.CHAR(26), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('followed_id', sa.CHAR(26), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now())
    )
    pass



def downgrade():
    op.drop_table('follows')
    pass