"""create_notifications_table

Revision ID: e87586e228aa
Revises: 7d5428f57960
Create Date: 2025-05-19 09:36:35.288270

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from app.enums.notification_enums import NotifiableType

# revision identifiers, used by Alembic.
revision = 'e87586e228aa'
down_revision = '7d5428f57960'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('notifications',
        sa.Column('id', sa.CHAR(26), primary_key=True),
        sa.Column('notifiable_id', sa.CHAR(26), nullable=False),
        sa.Column('notifiable_type', sa.Enum(*[e.value for e in NotifiableType], name='notifiable_types'), nullable=False),
        sa.Column('type', sa.Integer, nullable=False),
        sa.Column('title', sa.VARCHAR(50)),
        sa.Column('message', sa.VARCHAR(255), nullable=False),
        sa.Column('data', sa.Text),
        sa.Column('read_at', sa.DateTime),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_onupdate=sa.func.now())
    )
    pass


def downgrade():
    op.drop_table('notifications')
    pass