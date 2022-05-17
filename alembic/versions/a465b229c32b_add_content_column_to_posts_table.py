"""add content column to posts table

Revision ID: a465b229c32b
Revises: 9881f1f4c62e
Create Date: 2022-05-18 00:42:48.733643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a465b229c32b'
down_revision = '9881f1f4c62e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
