"""Add content column to posts table

Revision ID: dd596a3fb7f6
Revises: 581062ea028b
Create Date: 2021-11-26 08:47:44.935789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd596a3fb7f6'
down_revision = '581062ea028b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
