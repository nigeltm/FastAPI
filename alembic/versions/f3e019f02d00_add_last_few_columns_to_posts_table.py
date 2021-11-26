"""Add last few columns to posts table

Revision ID: f3e019f02d00
Revises: ef2aeefd6490
Create Date: 2021-11-26 09:22:37.400302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3e019f02d00'
down_revision = 'ef2aeefd6490'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column(
        'published',sa.Boolean(),nullable=False,server_default='True'),)
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')
    ),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')

    pass
