"""Add users table

Revision ID: e1bf716949b5
Revises: dd596a3fb7f6
Create Date: 2021-11-26 08:58:50.190580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1bf716949b5'
down_revision = 'dd596a3fb7f6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id',sa.Integer(),nullable=False),
    sa.Column('email',sa.String(),nullable=False),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
    server_default=sa.text('now()'),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
