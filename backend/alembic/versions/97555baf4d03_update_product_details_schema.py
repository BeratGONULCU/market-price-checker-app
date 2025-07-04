"""update product details schema

Revision ID: 97555baf4d03
Revises: 7e792aa26d93
Create Date: 2025-06-04 16:36:23.255284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97555baf4d03'
down_revision: Union[str, None] = '7e792aa26d93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_details', sa.Column('recorded_at', sa.DateTime(), nullable=False))
    op.add_column('product_details', sa.Column('last_updated', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product_details', 'last_updated')
    op.drop_column('product_details', 'recorded_at')
    # ### end Alembic commands ###
