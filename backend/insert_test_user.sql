-- Test kullanıcısı için şifre: test123
INSERT INTO users (name, email, password, created_at, updated_at)
VALUES (
    'Test User',
    'test@gmail.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYpR0.5J5J5J5J5', -- test123 şifresinin bcrypt hash'i
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
); 