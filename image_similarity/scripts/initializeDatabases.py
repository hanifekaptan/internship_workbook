import sqlite3
import os

DATASET_NAMES = ["wildlifeTiger"]
DB_FOLDER = "databases"


def createDatabase(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"'{db_path}' için tablolar oluşturuluyor...")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL UNIQUE,
            width INTEGER,
            height INTEGER,
            filesize_kb REAL
        )
        ''')
        print("  -> 'images' tablosu başarıyla oluşturuldu")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS similarities (
                image1 TEXT NOT NULL,
                image2 TEXT NOT NULL,
                cosine_score REAL NOT NULL,
                oklidean_score REAL NOT NULL,
                oklidean_with_faiss_score REAL NOT NULL,
                FOREIGN KEY (image1) REFERENCES images (id) ON DELETE CASCADE,
                FOREIGN KEY (image2) REFERENCES images (id) ON DELETE CASCADE,
                PRIMARY KEY (image1, image2)
            )
        """)
        print("  -> 'similarities' tablosu başarıyla oluşturuldu.")

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")


def main():
    print("Süreç başlatılıyor.")
    os.makedirs(DB_FOLDER, exist_ok=True)
    print(f"'{DB_FOLDER}' klasörü kontrol edildi\n")
    
    for db_name in DATASET_NAMES:
        database_path = os.path.join(DB_FOLDER, f"{db_name}.db")
        print(f"İşlemdeki veritabanı: {database_path}")
        createDatabase(database_path)
        print("-" * (28 + len(database_path)))
        print()

    print("İşlem tamamlandı.")


if __name__ == "__main__":
    main()