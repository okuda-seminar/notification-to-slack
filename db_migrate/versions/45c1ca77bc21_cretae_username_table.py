"""cretae username table

Revision ID: 45c1ca77bc21
Revises: 
Create Date: 2021-10-29 15:21:58.690721

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '45c1ca77bc21'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'usernames',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('slack_user_id', sa.String(100)),
        sa.Column('github_name', sa.String(100)),
        sa.Column('created_at', sa.DATETIME, default=datetime.now(), nullable=False),
        sa.Column('updated_at', sa.DATETIME, default=datetime.now(), nullable=False)
    )


def downgrade():
    op.drop_table('usernames')
