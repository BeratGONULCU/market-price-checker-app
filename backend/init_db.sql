-- Drop existing tables if they exist
DROP TABLE IF EXISTS user_settings CASCADE;
DROP TABLE IF EXISTS search_history CASCADE;
DROP TABLE IF EXISTS ratings CASCADE;
DROP TABLE IF EXISTS shopping_list_items CASCADE;
DROP TABLE IF EXISTS favorites CASCADE;
DROP TABLE IF EXISTS price_history CASCADE;
DROP TABLE IF EXISTS price_alerts CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS product_details CASCADE;
DROP TABLE IF EXISTS product_categories CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS markets CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS shopping_lists CASCADE;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255)
);

-- Create markets table
CREATE TABLE IF NOT EXISTS markets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(50),
    open_hours VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    image_url VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    brand VARCHAR(255),
    barcode VARCHAR(255),
    image_url VARCHAR(255),
    market_id INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_products_market
    FOREIGN KEY (market_id) REFERENCES markets(id)
);

-- Create product_categories table
CREATE TABLE IF NOT EXISTS product_categories (
    product_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (product_id, category_id)
);

-- Create product_details table
CREATE TABLE IF NOT EXISTS product_details (
    id SERIAL PRIMARY KEY,
    product_id INTEGER,
    market_id INTEGER,
    price DOUBLE PRECISION,
    expiration_date TIMESTAMP,
    calories DOUBLE PRECISION,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_details_product
    FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_product_details_market
    FOREIGN KEY (market_id) REFERENCES markets(id)
);

-- Create comments table
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    content VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Create favorites table
CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    title VARCHAR(255),
    message VARCHAR(255),
    type VARCHAR(255),
    is_read BOOLEAN,
    created_at TIMESTAMP,
    read_at TIMESTAMP
);

-- Create price_alerts table
CREATE TABLE IF NOT EXISTS price_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    target_price DOUBLE PRECISION,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    last_checked TIMESTAMP,
    notified BOOLEAN
);

-- Create price_history table
CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER,
    market_id INTEGER,
    price DOUBLE PRECISION,
    recorded_at TIMESTAMP
);

-- Create ratings table
CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Create search_history table
CREATE TABLE IF NOT EXISTS search_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    keyword VARCHAR(255),
    searched_at TIMESTAMP
);

-- Create shopping_list_items table
CREATE TABLE IF NOT EXISTS shopping_list_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    is_checked BOOLEAN
);

-- Create user_settings table
CREATE TABLE IF NOT EXISTS user_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    setting_key VARCHAR(255),
    value VARCHAR(255)
);

-- Create shopping_lists table
CREATE TABLE IF NOT EXISTS shopping_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_shopping_lists_user
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Add foreign key references
ALTER TABLE comments
ADD CONSTRAINT fk_comments_user
FOREIGN KEY (user_id) REFERENCES users(id),
ADD CONSTRAINT fk_comments_product
FOREIGN KEY (product_id) REFERENCES products(id);

ALTER TABLE favorites
ADD CONSTRAINT fk_favorites_user
FOREIGN KEY (user_id) REFERENCES users(id),
ADD CONSTRAINT fk_favorites_product
FOREIGN KEY (product_id) REFERENCES products(id);

ALTER TABLE notifications
ADD CONSTRAINT fk_notifications_user
FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE price_alerts
ADD CONSTRAINT fk_price_alerts_user
FOREIGN KEY (user_id) REFERENCES users(id),
ADD CONSTRAINT fk_price_alerts_product
FOREIGN KEY (product_id) REFERENCES products(id);

ALTER TABLE price_history
ADD CONSTRAINT fk_price_history_product
FOREIGN KEY (product_id) REFERENCES products(id),
ADD CONSTRAINT fk_price_history_market
FOREIGN KEY (market_id) REFERENCES markets(id);

ALTER TABLE product_categories
ADD CONSTRAINT fk_product_categories_product
FOREIGN KEY (product_id) REFERENCES products(id),
ADD CONSTRAINT fk_product_categories_category
FOREIGN KEY (category_id) REFERENCES categories(id);

ALTER TABLE ratings
ADD CONSTRAINT fk_ratings_user
FOREIGN KEY (user_id) REFERENCES users(id),
ADD CONSTRAINT fk_ratings_product
FOREIGN KEY (product_id) REFERENCES products(id);

ALTER TABLE search_history
ADD CONSTRAINT fk_search_history_user
FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE shopping_list_items
ADD CONSTRAINT fk_shopping_list_items_user
FOREIGN KEY (user_id) REFERENCES users(id),
ADD CONSTRAINT fk_shopping_list_items_product
FOREIGN KEY (product_id) REFERENCES products(id);

ALTER TABLE user_settings
ADD CONSTRAINT fk_user_settings_user
FOREIGN KEY (user_id) REFERENCES users(id);

-- Add created_at and updated_at columns to comments table
ALTER TABLE comments 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add created_at and updated_at columns to markets table
ALTER TABLE markets 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add created_at and updated_at columns to products table
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add created_at and updated_at columns to price_history table
ALTER TABLE price_history 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add created_at and updated_at columns to ratings table
ALTER TABLE ratings 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add created_at and updated_at columns to search_history table
ALTER TABLE search_history 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add created_at and updated_at columns to shopping_lists table
ALTER TABLE shopping_lists 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add created_at and updated_at columns to shopping_list_items table
ALTER TABLE shopping_list_items 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add created_at and updated_at columns to user_settings table
ALTER TABLE user_settings 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Add missing columns to categories table
ALTER TABLE categories 
ADD COLUMN IF NOT EXISTS parent_id INTEGER,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD CONSTRAINT fk_categories_parent 
FOREIGN KEY (parent_id) REFERENCES categories(id);

-- Modify column types
ALTER TABLE categories 
ALTER COLUMN name TYPE VARCHAR(100),
ALTER COLUMN description TYPE TEXT;

ALTER TABLE markets ADD COLUMN website VARCHAR(255);

-- Create triggers to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for each table
CREATE TRIGGER update_comments_updated_at
    BEFORE UPDATE ON comments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_markets_updated_at
    BEFORE UPDATE ON markets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_price_history_updated_at
    BEFORE UPDATE ON price_history
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ratings_updated_at
    BEFORE UPDATE ON ratings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_search_history_updated_at
    BEFORE UPDATE ON search_history
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_shopping_lists_updated_at
    BEFORE UPDATE ON shopping_lists
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_shopping_list_items_updated_at
    BEFORE UPDATE ON shopping_list_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_settings_updated_at
    BEFORE UPDATE ON user_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create trigger for categories table
CREATE OR REPLACE FUNCTION update_categories_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_categories_updated_at();

CREATE TRIGGER update_notifications_updated_at
    BEFORE UPDATE ON notifications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_price_alerts_updated_at
    BEFORE UPDATE ON price_alerts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_details_updated_at
    BEFORE UPDATE ON product_details
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_favorites_updated_at
    BEFORE UPDATE ON favorites
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE products ADD COLUMN market_id INTEGER;
ALTER TABLE products ADD CONSTRAINT fk_products_market FOREIGN KEY (market_id) REFERENCES markets(id);

-- Drop ratings table
DROP TABLE IF EXISTS ratings CASCADE;

-- Drop product_category table
DROP TABLE IF EXISTS product_category CASCADE;

-- Create notification type enum
CREATE TYPE notification_type AS ENUM ('price_alert', 'system', 'favorite', 'comment');

-- Modify notifications table to use enum
ALTER TABLE notifications 
ALTER COLUMN type TYPE notification_type USING type::notification_type;

-- Revert notification type enum
ALTER TABLE notifications 
ALTER COLUMN type TYPE character varying;

DROP TYPE IF EXISTS notification_type;

-- Recreate ratings table
CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Recreate product_category table
CREATE TABLE IF NOT EXISTS product_category (
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
); 