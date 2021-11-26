"""Add foreign key to posts table

Revision ID: ef2aeefd6490
Revises: e1bf716949b5
Create Date: 2021-11-26 09:15:27.919451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef2aeefd6490'
down_revision = 'e1bf716949b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fkey',source_table="posts",referent_table="users",
    local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
