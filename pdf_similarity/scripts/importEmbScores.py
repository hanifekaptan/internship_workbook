import pandas as pd
from src.utils.databaseManager import DatabaseManager
import os

def importEmbeddingScoresFromCsv(csvFilePath="similarity_results_emb.csv", dbName="similarity.db"):
    dbManager = None
    try:
        if not os.path.exists(csvFilePath):
            print(f"Hata: CSV dosyası bulunamadı: {csvFilePath}")
            return

        df = pd.read_csv(csvFilePath)
        dbManager = DatabaseManager(dbName=dbName)
        dbManager.connect()
        dbManager.createTables()
        scores_to_insert = df.to_dict(orient='records')
        dbManager.insertEmbeddingSimilarityScoresBatch(scores_to_insert)
        print(f"'{csvFilePath}' dosyasındaki {len(scores_to_insert)} embedding benzerlik skoru, '{dbName}' veritabanındaki 'embeddingSimilarityScores' tablosuna başarıyla aktarıldı.")

    except Exception as e:
        print(f"Veri aktarımı sırasında hata oluştu: {e}")
    finally:
        if dbManager: dbManager.close()

if __name__ == "__main__":
    importEmbeddingScoresFromCsv() 