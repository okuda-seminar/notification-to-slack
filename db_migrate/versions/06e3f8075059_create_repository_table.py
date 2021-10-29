"""create repository table

Revision ID: 06e3f8075059
Revises: f81d36fc0a31
Create Date: 2021-10-29 15:37:58.307146

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '06e3f8075059'
down_revision = 'f81d36fc0a31'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'repositories',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('repo_name', sa.String(100)),
        sa.Column('pr_id', sa.String(100)),
        sa.Column('pr_created_at', sa.DATETIME, default=datetime.now(), nullable=False),
        sa.Column('pr_updated_at', sa.DATETIME, default=datetime.now(), nullable=False)
        sa.Column('created_at', sa.DATETIME, default=datetime.now(), nullable=False),
        sa.Column('updated_at', sa.DATETIME, default=datetime.now(), nullable=False)
    )


def downgrade():
    op.drop_table('repositories')
