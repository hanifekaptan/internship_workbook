import sqlite3
import pandas as pd
from pathlib import Path
import sys

def view_random_samples(db_path: Path, table_name: str = 'similarities', num_samples: int = 100):
    if not db_path.exists():
        print(f"HATA: Veritabanı dosyası bulunamadı -> '{db_path}'")
        sys.exit(1)
    try:
        with sqlite3.connect(db_path) as conn:
            query = f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT {num_samples}"
            print(f"-> '{table_name}' tablosundan rastgele {num_samples} adet kayıt çekiliyor...")
            df = pd.read_sql_query(query, conn)
        print("-> Başarılı! Veriler DataFrame'e yüklendi.\n")
        if df.empty:
            print("UYARI: Tabloda hiç veri bulunamadı.")
        else:
            print("--- DataFrame Bilgileri ---")
            df.info()
            
            print("\nÖrnek Veriler")
            pd.set_option('display.max_rows', 100)
            pd.set_option('display.max_columns', 10)
            pd.set_option('display.width', 120)
            print(df)
            
    except sqlite3.OperationalError as e:
        print(f"\nVERİTABANI HATASI: Tablo '{table_name}' bulunamadı veya sorgu hatalı. Hata: {e}")
    except Exception as e:
        print(f"\nBEKLENMEDİK BİR HATA OLUŞTU: {e}")

if __name__ == "__main__":
    DATABASE_FILE_TO_INSPECT = r"databases\wildlifeTiger.db"
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    db_path = PROJECT_ROOT / DATABASE_FILE_TO_INSPECT    
    view_random_samples(db_path=db_path, num_samples=100)