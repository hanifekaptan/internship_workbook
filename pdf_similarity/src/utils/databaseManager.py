import sqlite3
import os

class DatabaseManager:
    def __init__(self, dbName="similarity.db"):
        self.dbName = dbName
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dbName)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Veritabanı bağlantı hatası: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def createTables(self):
        if not self.conn or not self.cursor:
            return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS pdfData (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pdfPath TEXT NOT NULL UNIQUE,
                    extractedText TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS similarityScores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pdfPath1 TEXT NOT NULL,
                    pdfPath2 TEXT NOT NULL,
                    tfidfSimilarity REAL,
                    doc2vecSimilarity REAL,
                    wordEmbeddingSimilarity REAL,
                    semanticSimilarity REAL,
                    tableSimilarity REAL,
                    FOREIGN KEY (pdfPath1) REFERENCES pdfData(pdfPath),
                    FOREIGN KEY (pdfPath2) REFERENCES pdfData(pdfPath),
                    UNIQUE(pdfPath1, pdfPath2)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS embeddingSimilarityScores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pdf1 TEXT NOT NULL,
                    pdf2 TEXT NOT NULL,
                    tfidfSimilarity REAL,
                    doc2vecSimilarity REAL,
                    wordEmbeddingSimilarity REAL,
                    semanticSimilarity REAL,
                    tableSimilarity REAL,
                    UNIQUE(pdf1, pdf2)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Tablo oluşturma hatası: {e}")

    def insertPdfData(self, pdfPath, extractedText):
        if not self.conn or not self.cursor:
            return
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO pdfData (pdfPath, extractedText) VALUES (?, ?)
            """, (pdfPath, extractedText))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"PDF verisi ekleme hatası: {e}")
            raise

    def getPdfData(self, pdfPath):
        if not self.conn or not self.cursor:
            return None
        try:
            self.cursor.execute("SELECT extractedText FROM pdfData WHERE pdfPath = ?", (pdfPath,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"PDF metni çekme hatası: {e}")
            return None

    def insertSimilarityScore(self, pdfPath1, pdfPath2, tfidfScore, doc2vecScore, wordEmbeddingScore, semanticScore, tableScore):
        if not self.conn or not self.cursor:
            return
        try:
            if pdfPath1 > pdfPath2:
                pdfPath1, pdfPath2 = pdfPath2, pdfPath1

            self.cursor.execute("""
                INSERT OR REPLACE INTO similarityScores (
                    pdfPath1, pdfPath2, tfidfSimilarity, doc2vecSimilarity,
                    wordEmbeddingSimilarity, semanticSimilarity, tableSimilarity
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (pdfPath1, pdfPath2, tfidfScore, doc2vecScore, wordEmbeddingScore, semanticScore, tableScore))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Benzerlik skoru ekleme hatası ({os.path.basename(pdfPath1)}, {os.path.basename(pdfPath2)}): {e}")

    def insertSimilarityScoresBatch(self, scoresBatch):
        if not self.conn or not self.cursor:
            return
        try:
            data_to_insert = []
            for score_tuple in scoresBatch:
                pdfPath1, pdfPath2, tfidfScore, doc2vecScore, wordEmbeddingScore, semanticScore, tableScore = score_tuple
                if pdfPath1 > pdfPath2:
                    pdfPath1, pdfPath2 = pdfPath2, pdfPath1
                data_to_insert.append((pdfPath1, pdfPath2, tfidfScore, doc2vecScore, wordEmbeddingScore, semanticScore, tableScore))
            
            self.cursor.executemany("""
                INSERT OR REPLACE INTO similarityScores (
                    pdfPath1, pdfPath2, tfidfSimilarity, doc2vecSimilarity,
                    wordEmbeddingSimilarity, semanticSimilarity, tableSimilarity
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data_to_insert)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Toplu benzerlik skoru ekleme hatası: {e}")

    def insertEmbeddingSimilarityScoresBatch(self, scoresBatch):
        if not self.conn or not self.cursor:
            return
        try:
            data_to_insert = []
            for score_dict in scoresBatch:
                pdf1 = score_dict['pdf1']
                pdf2 = score_dict['pdf2']
                tfidfSimilarity = score_dict.get('tfidfSimilarity')
                doc2vecSimilarity = score_dict.get('doc2vecSimilarity')
                wordEmbeddingSimilarity = score_dict.get('wordEmbeddingSimilarity')
                semanticSimilarity = score_dict.get('semanticSimilarity')
                tableSimilarity = score_dict.get('tableSimilarity')
                
                if pdf1 > pdf2:
                    pdf1, pdf2 = pdf2, pdf1

                data_to_insert.append((
                    pdf1, pdf2, tfidfSimilarity, doc2vecSimilarity, 
                    wordEmbeddingSimilarity, semanticSimilarity, tableSimilarity
                ))
            
            self.cursor.executemany("""
                INSERT OR REPLACE INTO embeddingSimilarityScores (
                    pdf1, pdf2, tfidfSimilarity, doc2vecSimilarity,
                    wordEmbeddingSimilarity, semanticSimilarity, tableSimilarity
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data_to_insert)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Toplu embedding benzerlik skoru ekleme hatası: {e}")

    def getSimilarityScores(self, pdfPath1, pdfPath2):
        if not self.conn or not self.cursor:
            return None
        try:
            if pdfPath1 > pdfPath2:
                pdfPath1, pdfPath2 = pdfPath2, pdfPath1

            self.cursor.execute("""
                SELECT tfidfSimilarity, doc2vecSimilarity, wordEmbeddingSimilarity, semanticSimilarity, tableSimilarity
                FROM similarityScores
                WHERE pdfPath1 = ? AND pdfPath2 = ?
            """, (pdfPath1, pdfPath2))
            result = self.cursor.fetchone()
            return result if result else None
        except sqlite3.Error as e:
            print(f"Benzerlik skorları çekme hatası: {e}")
            return None

    def getEmbeddingSimilarityScores(self, pdf1, pdf2):
        if not self.conn or not self.cursor:
            return None
        try:
            if pdf1 > pdf2:
                pdf1, pdf2 = pdf2, pdf1
            self.cursor.execute("""
                SELECT tfidfSimilarity, doc2vecSimilarity, wordEmbeddingSimilarity, semanticSimilarity, tableSimilarity
                FROM embeddingSimilarityScores
                WHERE pdf1 = ? AND pdf2 = ?
            """, (pdf1, pdf2))
            result = self.cursor.fetchone()
            return result if result else None
        except sqlite3.Error as e:
            print(f"Embedding benzerlik skorları çekme hatası: {e}")
            return None

    def getAllPdfPaths(self):
        if not self.conn or not self.cursor:
            return []
        try:
            self.cursor.execute("SELECT pdfPath FROM pdfData")
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Tüm PDF yollarını çekme hatası: {e}")
            return [] 