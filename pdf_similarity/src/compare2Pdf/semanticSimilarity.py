import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.preprocess import extractTextFromPdf

class SemanticSimilarity:
    def __init__(self):
        self.model = None
        self.corpus = {}
        self.pdfPaths = []
        self.pdfEmbeddings = {}
        self.modelName = 'all-MiniLM-L6-v2'

    def loadModel(self):
        if self.model is None:
            try:
                self.model = SentenceTransformer(self.modelName)
            except Exception as e:
                print(f"Hata: Sentence Transformer modeli yüklenirken bir sorun oluştu: {e}")
                self.model = None

    def addPdfToCorpus(self, pdfPath):
        text = extractTextFromPdf(pdfPath)
        if text:
            self.corpus[pdfPath] = text
            self.pdfPaths.append(pdfPath)

    def getEmbedding(self, pdfPath):
        if self.model is None:
            self.loadModel()
            if self.model is None:
                return None

        if pdfPath not in self.corpus:
            return None

        if pdfPath in self.pdfEmbeddings:
            return self.pdfEmbeddings[pdfPath]

        text = self.corpus[pdfPath]
        try:
            embedding = self.model.encode(text)
            self.pdfEmbeddings[pdfPath] = embedding
            return embedding
        except Exception as e:
            print(f"Hata: PDF ({pdfPath}) için embedding oluşturulurken sorun oluştu: {e}")
            return None

    def getSimilarity(self, pdfPath1, pdfPath2):
        if self.model is None:
            self.loadModel()
            if self.model is None:
                return None
        if pdfPath1 not in self.corpus or pdfPath2 not in self.corpus:
            return None

        embedding1 = self.getEmbedding(pdfPath1)
        embedding2 = self.getEmbedding(pdfPath2)

        if embedding1 is None or embedding2 is None:
            return None

        similarity_score = cosine_similarity(embedding1.reshape(1, -1), embedding2.reshape(1, -1))[0][0]
        return similarity_score

    def getMostSimilar(self, targetPdfPath, topN=5):
        if self.model is None:
            self.loadModel()
            if self.model is None:
                return []
        if targetPdfPath not in self.corpus:
            return []

        targetEmbedding = self.getEmbedding(targetPdfPath)
        if targetEmbedding is None:
            return []

        similarity_scores = []
        for path in self.pdfPaths:
            if path == targetPdfPath:
                continue
            candidateEmbedding = self.getEmbedding(path)
            if candidateEmbedding is not None:
                score = cosine_similarity(targetEmbedding.reshape(1, -1), candidateEmbedding.reshape(1, -1))[0][0]
                similarity_scores.append((path, score))
        
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        return similarity_scores[:topN] 