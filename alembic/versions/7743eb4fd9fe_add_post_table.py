"""Add Post table

Revision ID: 7743eb4fd9fe
Revises: 3e47e098f313
Create Date: 2023-07-30 21:35:29.580049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7743eb4fd9fe'
down_revision = '3e47e098f313'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String),
        sa.Column('content', sa.String),
        sa.Column('is_public', sa.Boolean),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column('likes', sa.Integer, server_default="0"),
        sa.Column('dislikes', sa.Integer, server_default="0")
    )


def downgrade() -> None:
    op.drop_table('posts')
