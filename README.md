# Market Price Comparison Full Stack

Bu proje, market ürünlerinin fiyatlarını karşılaştırmak için geliştirilmiş bir full-stack uygulamadır.

## Proje Yapısı

- `backend/`: FastAPI ile geliştirilmiş backend
- `frontend/`: React ile geliştirilmiş frontend

## Kurulum

### Backend Kurulumu

1. Python 3.8+ yükleyin
2. PostgreSQL yükleyin ve çalıştırın
3. Backend klasörüne gidin:
   ```bash
   cd backend
   ```
4. Sanal ortam oluşturun ve aktifleştirin:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
5. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
6. Veritabanını oluşturun:
   - PostgreSQL'de `market_db` adında yeni bir veritabanı oluşturun
   - `init_db.sql` dosyasını çalıştırın

7. Uygulamayı başlatın:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Kurulumu

1. Node.js yükleyin
2. Frontend klasörüne gidin:
   ```bash
   cd frontend
   ```
3. Bağımlılıkları yükleyin:
   ```bash
   npm install
   ```
4. Uygulamayı başlatın:
   ```bash
   npm start
   ```

## Veritabanı Ayarları

Backend'de `app/core/config.py` dosyasında veritabanı bağlantı ayarlarını güncelleyin:

```python
POSTGRES_SERVER: str = "localhost"
POSTGRES_USER: str = "postgres"
POSTGRES_PASSWORD: str = "your_password"
POSTGRES_DB: str = "market_db"
```

## Lisans

MIT 