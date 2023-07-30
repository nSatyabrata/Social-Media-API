"""Add user table

Revision ID: 3e47e098f313
Revises: 
Create Date: 2023-07-30 20:51:33.816482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e47e098f313'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('users')
