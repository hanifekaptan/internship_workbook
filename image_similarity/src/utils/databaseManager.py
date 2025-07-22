import sqlite3
from typing import List, Dict, Any

class DatabaseManager:

    def __init__(self, db_path: str):
        if not db_path:
            raise ValueError("Veritabanı yolu (db_path) belirtilmelidir.")
        self.db_path = db_path

    def insertMany(self, table_name: str, data: List[Dict[str, Any]]):
        if not data:
            print("Uyarı: Eklenecek veri bulunamadı. İşlem atlanıyor.")
            return
        columns = list(data[0].keys())
        column_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        sql_query = f"INSERT OR IGNORE INTO {table_name} ({column_str}) VALUES ({placeholders})"
        values_to_insert = [tuple(row[col] for col in columns) for row in data]
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(sql_query, values_to_insert)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Veritabanı Hatası: '{table_name}' tablosuna veri eklenirken sorun oluştu. Hata: {e}")


    def selectFilepaths(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, filepath FROM images")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Veritabanı Hatası: 'images' tablosundan dosya yolları alınırken sorun oluştu. Hata: {e}")
            return []