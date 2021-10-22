"""create username table

Revision ID: 22b0f490c69b
Revises: 43721fcf71e2
Create Date: 2021-10-22 15:25:08.920306

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '22b0f490c69b'
down_revision = '43721fcf71e2'
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
    pass


def downgrade():
    op.drop_table('usernames')
    pass
