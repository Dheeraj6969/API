"""add foreign key to post table

Revision ID: 5653530e5add
Revises: 60b64258f98a
Create Date: 2022-05-18 00:56:22.547461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5653530e5add'
down_revision = '60b64258f98a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
