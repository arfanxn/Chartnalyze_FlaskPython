"""create permissions table

Revision ID: 50c3059cc908
Revises: 7c9d01fa4f14
Create Date: 2025-04-29 14:49:01.138241

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '50c3059cc908'
down_revision = '7c9d01fa4f14'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('permissions',
        sa.Column('id', sa.CHAR(length=26), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime),
    )

def downgrade():
    op.drop_table('permissions')   