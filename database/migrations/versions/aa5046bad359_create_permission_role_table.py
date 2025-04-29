"""create permission_role table

Revision ID: aa5046bad359
Revises: 602e94c6a08d
Create Date: 2025-04-29 15:05:20.081654

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aa5046bad359'
down_revision = '602e94c6a08d'
branch_labels = None
depends_on = None

def upgrade():
    
    op.create_table('permission_role',
        sa.Column('permission_id', sa.CHAR(length=26), sa.ForeignKey('permissions.id'), nullable=False),
        sa.Column('role_id', sa.CHAR(length=26), sa.ForeignKey('roles.id'), nullable=False),
    )

def downgrade():
    op.drop_table('permission_role')   