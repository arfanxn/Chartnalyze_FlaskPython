"""create_medias_table

Revision ID: 0398109cca9f
Revises: 68d5fa430e52
Create Date: 2025-05-19 10:17:19.832323

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from app.enums.media_enums import ModelType

# revision identifiers, used by Alembic.
revision = '0398109cca9f'
down_revision = '68d5fa430e52'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('medias',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('model_id', sa.CHAR(26), nullable=False),
        sa.Column('model_type', sa.Enum(*[e.value for e in ModelType], name='model_types'), nullable=False),
        sa.Column('collection_name', sa.VARCHAR(50), nullable=False),
        sa.Column('name', sa.VARCHAR(50), nullable=False),
        sa.Column('file_name', sa.VARCHAR(255), nullable=False),
        sa.Column('mime_type', sa.VARCHAR(50), nullable=False),
        sa.Column('disk', sa.VARCHAR(50)),
        sa.Column('size', sa.BigInteger, nullable=False),
        sa.Column('data', sa.JSON),
        sa.Column('order', sa.Integer), # order in collection
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )
    pass


def downgrade():
    op.drop_table('medias')
    pass