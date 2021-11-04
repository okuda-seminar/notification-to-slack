"""create username table

Revision ID: ea8fd9e4b7e9
Revises: a9b4f97c9dea
Create Date: 2021-11-01 17:11:28.983184

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'ea8fd9e4b7e9'
down_revision = 'a9b4f97c9dea'
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
