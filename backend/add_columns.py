from sqlalchemy import create_engine, text
from app.core.config import settings
import os

def add_columns():
    try:
        # Veritabanı bağlantısını oluştur
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
        
        # SQL dosyasını oku
        sql_file_path = os.path.join(os.path.dirname(__file__), 'add_columns.sql')
        with open(sql_file_path, 'r') as file:
            sql_commands = file.read()
        
        # SQL komutlarını çalıştır
        with engine.connect() as connection:
            connection.execute(text(sql_commands))
            connection.commit()
            print("Kolonlar başarıyla eklendi!")
            
    except Exception as e:
        print(f"Hata: {str(e)}")

if __name__ == "__main__":
    add_columns() 