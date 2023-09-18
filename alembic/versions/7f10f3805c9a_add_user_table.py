"""add user table

Revision ID: 7f10f3805c9a
Revises: 6ff578228d2f
Create Date: 2023-09-18 20:44:18.198240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f10f3805c9a'
down_revision: Union[str, None] = '6ff578228d2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                            sa.Column("email", sa.String, nullable=False),
                            sa.Column("password", sa.String, nullable=False),
                            sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                            sa.PrimaryKeyConstraint("id"),
                            sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
