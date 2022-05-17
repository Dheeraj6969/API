"""Create Posts Table

Revision ID: 9881f1f4c62e
Revises: 
Create Date: 2022-05-18 00:31:36.841163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9881f1f4c62e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
