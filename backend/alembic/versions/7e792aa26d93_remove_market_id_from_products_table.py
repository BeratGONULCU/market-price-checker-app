"""remove market_id from products table

Revision ID: 7e792aa26d93
Revises: 
Create Date: 2025-06-04 15:42:21.557013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7e792aa26d93'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'content',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('comments', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('comments', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.add_column('favorites', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('favorites', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('favorites', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('favorites', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_index(op.f('ix_favorites_id'), 'favorites', ['id'], unique=False)
    op.alter_column('markets', 'name',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.alter_column('markets', 'phone',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=20),
               existing_nullable=True)
    op.alter_column('markets', 'open_hours',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.create_index(op.f('ix_markets_id'), 'markets', ['id'], unique=False)
    op.add_column('notifications', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('notifications', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('notifications', 'title',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('notifications', 'message',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('notifications', 'type',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('notifications', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=False)
    op.add_column('price_alerts', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('price_alerts', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('price_alerts', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('price_alerts', 'target_price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('price_alerts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.create_index(op.f('ix_price_alerts_id'), 'price_alerts', ['id'], unique=False)
    op.alter_column('price_history', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.create_index(op.f('ix_price_history_id'), 'price_history', ['id'], unique=False)
    op.drop_column('price_history', 'recorded_at')
    op.alter_column('product_details', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('product_details', 'market_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('product_details', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('product_details', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('product_details', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.create_index(op.f('ix_product_details_id'), 'product_details', ['id'], unique=False)
    op.alter_column('products', 'name',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.alter_column('products', 'brand',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.alter_column('products', 'barcode',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=50),
               existing_nullable=True)
    op.create_index(op.f('ix_products_barcode'), 'products', ['barcode'], unique=True)
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.drop_constraint('fk_products_market', 'products', type_='foreignkey')
    op.drop_column('products', 'market_id')
    op.alter_column('ratings', 'rating',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               nullable=False)
    op.alter_column('ratings', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.create_index(op.f('ix_ratings_id'), 'ratings', ['id'], unique=False)
    op.drop_column('ratings', 'comment')
    op.add_column('search_history', sa.Column('query', sa.String(length=255), nullable=False))
    op.create_index(op.f('ix_search_history_id'), 'search_history', ['id'], unique=False)
    op.drop_column('search_history', 'keyword')
    op.drop_column('search_history', 'searched_at')
    op.add_column('shopping_list_items', sa.Column('shopping_list_id', sa.Integer(), nullable=True))
    op.add_column('shopping_list_items', sa.Column('quantity', sa.Integer(), nullable=True))
    op.add_column('shopping_list_items', sa.Column('notes', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_shopping_list_items_id'), 'shopping_list_items', ['id'], unique=False)
    op.drop_constraint('fk_shopping_list_items_user', 'shopping_list_items', type_='foreignkey')
    op.create_foreign_key(None, 'shopping_list_items', 'shopping_lists', ['shopping_list_id'], ['id'])
    op.drop_column('shopping_list_items', 'is_checked')
    op.drop_column('shopping_list_items', 'user_id')
    op.alter_column('shopping_lists', 'name',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.create_index(op.f('ix_shopping_lists_id'), 'shopping_lists', ['id'], unique=False)
    op.alter_column('user_settings', 'setting_key',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=50),
               nullable=False)
    op.create_index(op.f('ix_user_settings_id'), 'user_settings', ['id'], unique=False)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.alter_column('users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_index(op.f('ix_user_settings_id'), table_name='user_settings')
    op.alter_column('user_settings', 'setting_key',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_index(op.f('ix_shopping_lists_id'), table_name='shopping_lists')
    op.alter_column('shopping_lists', 'name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.add_column('shopping_list_items', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('shopping_list_items', sa.Column('is_checked', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'shopping_list_items', type_='foreignkey')
    op.create_foreign_key('fk_shopping_list_items_user', 'shopping_list_items', 'users', ['user_id'], ['id'])
    op.drop_index(op.f('ix_shopping_list_items_id'), table_name='shopping_list_items')
    op.drop_column('shopping_list_items', 'notes')
    op.drop_column('shopping_list_items', 'quantity')
    op.drop_column('shopping_list_items', 'shopping_list_id')
    op.add_column('search_history', sa.Column('searched_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('search_history', sa.Column('keyword', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_search_history_id'), table_name='search_history')
    op.drop_column('search_history', 'query')
    op.add_column('ratings', sa.Column('comment', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_ratings_id'), table_name='ratings')
    op.alter_column('ratings', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('ratings', 'rating',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               nullable=True)
    op.add_column('products', sa.Column('market_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_products_market', 'products', 'markets', ['market_id'], ['id'])
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_index(op.f('ix_products_barcode'), table_name='products')
    op.alter_column('products', 'barcode',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    op.alter_column('products', 'brand',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    op.alter_column('products', 'name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.drop_index(op.f('ix_product_details_id'), table_name='product_details')
    op.alter_column('product_details', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('product_details', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('product_details', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('product_details', 'market_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('product_details', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('price_history', sa.Column('recorded_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_price_history_id'), table_name='price_history')
    op.alter_column('price_history', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.drop_index(op.f('ix_price_alerts_id'), table_name='price_alerts')
    op.alter_column('price_alerts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('price_alerts', 'target_price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('price_alerts', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('price_alerts', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('price_alerts', 'updated_at')
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.alter_column('notifications', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('notifications', 'type',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('notifications', 'message',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('notifications', 'title',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('notifications', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('notifications', 'updated_at')
    op.drop_index(op.f('ix_markets_id'), table_name='markets')
    op.alter_column('markets', 'open_hours',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    op.alter_column('markets', 'phone',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    op.alter_column('markets', 'name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.drop_index(op.f('ix_favorites_id'), table_name='favorites')
    op.alter_column('favorites', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('favorites', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('favorites', 'updated_at')
    op.drop_column('favorites', 'created_at')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.alter_column('comments', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('comments', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('comments', 'content',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('comments', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    # ### end Alembic commands ###
