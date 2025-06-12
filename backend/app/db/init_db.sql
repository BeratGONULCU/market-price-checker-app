-- Kullanıcılar tablosu
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Kategoriler tablosu
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Marketler tablosu
CREATE TABLE IF NOT EXISTS markets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    logo_url VARCHAR(255),
    website VARCHAR(255),
    address TEXT,
    phone VARCHAR(50),
    open_hours TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Ürünler tablosu
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    brand VARCHAR(255),
    barcode VARCHAR(255) UNIQUE,
    image_url VARCHAR(255),
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Ürün detayları tablosu
CREATE TABLE IF NOT EXISTS product_details (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    market_id INTEGER REFERENCES markets(id),
    price DECIMAL(10,2) NOT NULL,
    unit VARCHAR(50),
    expiration_date DATE,
    calories INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, market_id)
);

-- Favoriler tablosu
CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, product_id)
);

-- Alışveriş listeleri tablosu
CREATE TABLE IF NOT EXISTS shopping_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Alışveriş listesi öğeleri tablosu
CREATE TABLE IF NOT EXISTS shopping_list_items (
    id SERIAL PRIMARY KEY,
    shopping_list_id INTEGER REFERENCES shopping_lists(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    is_checked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(shopping_list_id, product_id)
);

-- Yorumlar tablosu
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    content TEXT NOT NULL,
    rating DECIMAL(2,1) NOT NULL CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Fiyat geçmişi tablosu
CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    market_id INTEGER REFERENCES markets(id),
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Fiyat alarmları tablosu
CREATE TABLE IF NOT EXISTS price_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    target_price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, product_id)
);

-- İndeksler
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_product_details_product ON product_details(product_id);
CREATE INDEX IF NOT EXISTS idx_product_details_market ON product_details(market_id);
CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_product ON favorites(product_id);
CREATE INDEX IF NOT EXISTS idx_shopping_lists_user ON shopping_lists(user_id);
CREATE INDEX IF NOT EXISTS idx_shopping_list_items_list ON shopping_list_items(shopping_list_id);
CREATE INDEX IF NOT EXISTS idx_shopping_list_items_product ON shopping_list_items(product_id);
CREATE INDEX IF NOT EXISTS idx_comments_product ON comments(product_id);
CREATE INDEX IF NOT EXISTS idx_comments_user ON comments(user_id);
CREATE INDEX IF NOT EXISTS idx_price_history_product ON price_history(product_id);
CREATE INDEX IF NOT EXISTS idx_price_history_market ON price_history(market_id);
CREATE INDEX IF NOT EXISTS idx_price_alerts_user ON price_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_price_alerts_product ON price_alerts(product_id);

-- Trigger fonksiyonu - updated_at alanını güncellemek için
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger'lar
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at
    BEFORE UPDATE ON categories
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

CREATE TRIGGER update_product_details_updated_at
    BEFORE UPDATE ON product_details
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

CREATE TRIGGER update_comments_updated_at
    BEFORE UPDATE ON comments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_price_alerts_updated_at
    BEFORE UPDATE ON price_alerts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments tablosuna rating kolonu ekle
ALTER TABLE comments 
    ADD COLUMN IF NOT EXISTS rating DECIMAL(2,1) NOT NULL CHECK (rating >= 1 AND rating <= 5); 