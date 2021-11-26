"""create posts table

Revision ID: 581062ea028b
Revises: 
Create Date: 2021-11-26 08:37:55.123926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '581062ea028b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
    ,sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
