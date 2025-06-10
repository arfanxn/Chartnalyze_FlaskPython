"""create_activities_table

Revision ID: cb0f94e234f5
Revises: 0398109cca9f
Create Date: 2025-06-10 11:15:15.666584

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from app.enums.activity_enums import CauserType, SubjectType, Type

# revision identifiers, used by Alembic.
revision = 'cb0f94e234f5'
down_revision = '0398109cca9f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('activities',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('type', sa.Enum(*[e.value for e in Type], name='types'), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('subject_id', sa.CHAR(26)),
        sa.Column('subject_type', sa.Enum(*[e.value for e in SubjectType], name='subject_types')),
        sa.Column('causer_id', sa.CHAR(26)),
        sa.Column('causer_type', sa.Enum(*[e.value for e in CauserType], name='causer_types')),
        sa.Column('properties', sa.JSON),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now())
    )
    pass


def downgrade():
    
    op.drop_table('activities')
    pass