"""Add Likes table

Revision ID: c3cad8d2e621
Revises: 7743eb4fd9fe
Create Date: 2023-07-30 22:00:18.456990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3cad8d2e621'
down_revision = '7743eb4fd9fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('likes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('like_post', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )


def downgrade() -> None:
    op.drop_table('likes')
