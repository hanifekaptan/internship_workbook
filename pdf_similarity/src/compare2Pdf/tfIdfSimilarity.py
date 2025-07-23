import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.preprocess import extractTextFromPdf

class TfidfSimilarity:
    def __init__(self):
        self.corpus = {}
        self.vectorizer = TfidfVectorizer()
        self.tfidfMatrix = None
        self.pdfPaths = []

    def addPdfToCorpus(self, pdfPath):
        text = extractTextFromPdf(pdfPath)
        if text:
            self.corpus[pdfPath] = text
            self.pdfPaths.append(pdfPath)

    def buildTfidfModel(self):
        if not self.corpus:
            return
        texts = [self.corpus[path] for path in self.pdfPaths]
        self.tfidfMatrix = self.vectorizer.fit_transform(texts)

    def getSimilarity(self, pdfPath1, pdfPath2):
        if pdfPath1 not in self.corpus or pdfPath2 not in self.corpus:
            return None
        if self.tfidfMatrix is None:
            return None

        try:
            idx1 = self.pdfPaths.index(pdfPath1)
            idx2 = self.pdfPaths.index(pdfPath2)
            
            vector1 = self.tfidfMatrix.getrow(idx1).toarray()
            vector2 = self.tfidfMatrix.getrow(idx2).toarray()

            similarity_score = cosine_similarity(vector1, vector2)[0][0]
            return similarity_score
        except Exception as e:
            return None

    def getMostSimilar(self, targetPdfPath, topN=5):
        if targetPdfPath not in self.corpus:
            return []
        if self.tfidfMatrix is None:
            return []

        try:
            targetIdx = self.pdfPaths.index(targetPdfPath)
            targetVector = self.tfidfMatrix.getrow(targetIdx).toarray()
            
            similarity_scores = []
            for i, pdfPath in enumerate(self.pdfPaths):
                if pdfPath == targetPdfPath:
                    continue
                candidateVector = self.tfidfMatrix.getrow(i).toarray()
                score = cosine_similarity(targetVector, candidateVector)[0][0]
                similarity_scores.append((pdfPath, score))
            
            similarity_scores.sort(key=lambda x: x[1], reverse=True)
            return similarity_scores[:topN]
        except Exception as e:
            print(f"TF-IDF en benzer PDF'ler bulunurken hata oluştu: {e}")
            return [] 