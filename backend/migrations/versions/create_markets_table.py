"""create markets table

Revision ID: create_markets_table
Revises: create_product_details_table
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_markets_table'
down_revision = 'create_product_details_table'
branch_labels = None
depends_on = None


def upgrade():
    # Create markets table
    op.create_table(
        'markets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add is_favorite column to product_details table
    op.add_column('product_details', sa.Column('is_favorite', sa.Boolean(), nullable=False, server_default='false'))


def downgrade():
    # Drop markets table
    op.drop_table('markets')
    
    # Remove is_favorite column from product_details table
    op.drop_column('product_details', 'is_favorite') 