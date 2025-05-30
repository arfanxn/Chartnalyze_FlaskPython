"""create roles table

Revision ID: 7c9d01fa4f14
Revises: 5472b5f1f82b
Create Date: 2025-04-29 14:43:57.682296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7c9d01fa4f14'
down_revision = '5472b5f1f82b'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('roles',
        sa.Column('id', sa.CHAR(length=26), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now()),
    )

def downgrade():
    op.drop_table('roles')   