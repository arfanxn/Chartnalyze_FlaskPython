"""create_countries_table

Revision ID: 5472b5f1f82b
Revises: None
Create Date: 2025-05-19 09:25:42.249818

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5472b5f1f82b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('countries',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('name', sa.VARCHAR(50), nullable=False),
        sa.Column('iso_code', sa.CHAR(2), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now()),
    )
    pass


def downgrade():
    op.drop_table('countries')
    pass