"""create repository table

Revision ID: a9b4f97c9dea
Revises:
Create Date: 2021-11-01 17:06:38.623546

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'a9b4f97c9dea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'repositories',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('repo_name', sa.String(100)),
        sa.Column('pr_id', sa.String(100)),
        sa.Column('pr_created_at', sa.DATETIME, default=datetime.now(), nullable=False),
        sa.Column('pr_updated_at', sa.DATETIME, default=datetime.now(), nullable=False),
        sa.Column('created_at', sa.DATETIME, default=datetime.now(), nullable=False),
        sa.Column('updated_at', sa.DATETIME, default=datetime.now(), nullable=False))


def downgrade():
    op.drop_table('repositories')
