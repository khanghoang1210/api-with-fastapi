"""add column content to posts table

Revision ID: 6ff578228d2f
Revises: a927d3f38710
Create Date: 2023-09-18 20:38:33.450785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ff578228d2f'
down_revision: Union[str, None] = 'a927d3f38710'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
