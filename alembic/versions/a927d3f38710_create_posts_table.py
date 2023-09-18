"""create posts table

Revision ID: a927d3f38710
Revises: 
Create Date: 2023-09-18 20:27:25.720827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a927d3f38710'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                      sa.Column("title", sa.String(), nullable=False))


def downgrade() -> None:
    pass
