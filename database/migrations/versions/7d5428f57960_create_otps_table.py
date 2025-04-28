"""create otps table

Revision ID: 7d5428f57960
Revises: 2492258395c3
Create Date: 2025-04-26 13:42:01.905529

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d5428f57960'
down_revision = '2492258395c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('otps',
        sa.Column('id', sa.CHAR(length=26), primary_key=True),
        sa.Column('email', sa.String(length=50), nullable=False),
        sa.Column('code', sa.Integer, nullable=False),  # 6 digits OTP code, don't start with 0 to avoid truncation
        sa.Column('used_at', sa.DateTime, nullable=True),
        sa.Column('revoked_at', sa.DateTime, nullable=True),
        sa.Column('expired_at', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
    )
    pass


def downgrade():
    op.drop_table('otps')   