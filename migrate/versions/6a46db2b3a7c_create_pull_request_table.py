"""create pull request table

Revision ID: 6a46db2b3a7c
Revises: ea8fd9e4b7e9
Create Date: 2021-11-01 17:12:27.929566

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '6a46db2b3a7c'
down_revision = 'ea8fd9e4b7e9'
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
