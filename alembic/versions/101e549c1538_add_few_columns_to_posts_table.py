"""add few columns to posts table

Revision ID: 101e549c1538
Revises: b3a275d67275
Create Date: 2023-09-18 21:03:22.873791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '101e549c1538'
down_revision: Union[str, None] = 'b3a275d67275'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column( "posts", sa.Column("published",sa.Boolean, server_default='TRUE', nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                                                                    server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
