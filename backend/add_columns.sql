-- Add created_at and updated_at columns to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Create trigger to update updated_at column
CREATE OR REPLACE FUNCTION update_users_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_users_updated_at();

-- shopping_list_items tablosuna is_checked kolonu ekle
ALTER TABLE shopping_list_items ADD COLUMN IF NOT EXISTS is_checked BOOLEAN DEFAULT FALSE;

-- shopping_lists tablosuna is_checked kolonu ekle (eğer gerekirse)
ALTER TABLE shopping_lists ADD COLUMN IF NOT EXISTS is_checked BOOLEAN DEFAULT FALSE; 