"""add forein key for posts table

Revision ID: b3a275d67275
Revises: 7f10f3805c9a
Create Date: 2023-09-18 20:54:31.462260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3a275d67275'
down_revision: Union[str, None] = '7f10f3805c9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts","owner_id")
    pass
