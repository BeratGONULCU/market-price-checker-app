-- Test verisi ekle

-- Önce shopping_list_items tablosuna is_checked kolonu ekle (eğer yoksa)
ALTER TABLE shopping_list_items ADD COLUMN IF NOT EXISTS is_checked BOOLEAN DEFAULT FALSE;

-- Test marketleri ekle
INSERT INTO markets (name, address, phone, open_hours, latitude, longitude, website, created_at, updated_at) VALUES
('Migros', 'Kadıköy, İstanbul', '0216 123 45 67', '08:00-22:00', 40.9909, 29.0303, 'https://www.migros.com.tr', NOW(), NOW()),
('Carrefour', 'Beşiktaş, İstanbul', '0212 987 65 43', '07:00-23:00', 41.0422, 29.0083, 'https://www.carrefour.com.tr', NOW(), NOW()),
('A101', 'Şişli, İstanbul', '0212 555 12 34', '06:00-24:00', 41.0602, 28.9877, 'https://www.a101.com.tr', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Test ürünleri ekle
INSERT INTO products (name, description, brand, image_url, barcode, created_at, updated_at) VALUES
('Süt', 'Tam yağlı süt', 'Sütaş', 'https://example.com/sut.jpg', '123456789', NOW(), NOW()),
('Ekmek', 'Beyaz ekmek', 'Ülker', 'https://example.com/ekmek.jpg', '987654321', NOW(), NOW()),
('Yumurta', 'Çiftlik yumurtası', 'Köy Yumurtası', 'https://example.com/yumurta.jpg', '456789123', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Test product_details ekle
INSERT INTO product_details (product_id, market_id, price, expiration_date, calories, created_at, updated_at, is_favorite) VALUES
(1, 1, 15.50, '2024-02-15', 120, NOW(), NOW(), false),
(1, 2, 16.00, '2024-02-15', 120, NOW(), NOW(), false),
(1, 3, 14.90, '2024-02-15', 120, NOW(), NOW(), false),
(2, 1, 8.50, '2024-02-10', 250, NOW(), NOW(), false),
(2, 2, 8.00, '2024-02-10', 250, NOW(), NOW(), false),
(2, 3, 7.90, '2024-02-10', 250, NOW(), NOW(), false),
(3, 1, 25.00, '2024-02-20', 70, NOW(), NOW(), false),
(3, 2, 24.50, '2024-02-20', 70, NOW(), NOW(), false),
(3, 3, 23.90, '2024-02-20', 70, NOW(), NOW(), false)
ON CONFLICT (id) DO NOTHING;

-- Test shopping_list ekle (eğer yoksa)
INSERT INTO shopping_lists (user_id, name, created_at, updated_at) VALUES
(1, 'Test Alışveriş Listesi', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Test shopping_list_items ekle
INSERT INTO shopping_list_items (shopping_list_id, product_id, quantity, notes, created_at, updated_at, is_checked) VALUES
(5, 1, 2, 'Tam yağlı olsun', NOW(), NOW(), false),
(5, 2, 1, 'Taze olsun', NOW(), NOW(), false),
(5, 3, 1, 'Büyük boy', NOW(), NOW(), false)
ON CONFLICT (id) DO NOTHING; 