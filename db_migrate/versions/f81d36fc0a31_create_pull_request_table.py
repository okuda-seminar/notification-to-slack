"""create pull request table

Revision ID: f81d36fc0a31
Revises: 45c1ca77bc21
Create Date: 2021-10-29 15:32:18.092140

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'f81d36fc0a31'
down_revision = '45c1ca77bc21'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pull_requests',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('pr_id', sa.String(100)),
        sa.Column('pr_number', sa.Integer),
        sa.Column('pr_title', sa.String(100)),
        sa.Column('pr_reviewer', sa.String(100)),
        sa.Column('pr_url', sa.String(100)),
        sa.Column('created_at', sa.DATETIME, default=datetime.now(), nullable=False),
        sa.Column('updated_at', sa.DATETIME, default=datetime.now(), nullable=False)
    )


def downgrade():
    op.drop_table('pull_requests')
