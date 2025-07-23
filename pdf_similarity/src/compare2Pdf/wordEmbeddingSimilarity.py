import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.preprocess import extractTextFromPdf

class WordEmbeddingSimilarity:
    def __init__(self):
        self.corpus = {}
        self.pdfPaths = []
        self.tokenizedCorpus = []
        self.word2vecModel = None

    def addPdfToCorpus(self, pdfPath):
        text = extractTextFromPdf(pdfPath)
        if text:
            self.corpus[pdfPath] = text
            self.pdfPaths.append(pdfPath)
            self.tokenizedCorpus.append(text.lower().split())

    def buildWordEmbeddingModel(self, vectorSize=100, window=5, minCount=1, workers=4, epochs=10):
        if not self.tokenizedCorpus:
            return
        self.word2vecModel = Word2Vec(self.tokenizedCorpus, vector_size=vectorSize, window=window, min_count=minCount, workers=workers, epochs=epochs)

    def _getDocumentVector(self, pdfPath):
        if self.word2vecModel is None:
            return None
        if pdfPath not in self.corpus:
            return None

        text = self.corpus[pdfPath]
        tokens = text.lower().split()
        
        validVectors = []
        for word in tokens:
            if word in self.word2vecModel.wv:
                validVectors.append(self.word2vecModel.wv[word])

        if not validVectors:
            return np.zeros(self.word2vecModel.vector_size)

        return np.mean(validVectors, axis=0)

    def getSimilarity(self, pdfPath1, pdfPath2):
        if self.word2vecModel is None:
            return None
        if pdfPath1 not in self.corpus or pdfPath2 not in self.corpus:
            return None

        vec1 = self._getDocumentVector(pdfPath1)
        vec2 = self._getDocumentVector(pdfPath2)

        if vec1 is None or vec2 is None:
            return None

        similarity_score = cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
        return similarity_score

    def getMostSimilar(self, targetPdfPath, topN=5):
        if self.word2vecModel is None:
            return []
        if targetPdfPath not in self.corpus:
            return []

        targetVector = self._getDocumentVector(targetPdfPath)
        if targetVector is None:
            return []

        similarity_scores = []
        for path in self.pdfPaths:
            if path == targetPdfPath:
                continue
            candidateVector = self._getDocumentVector(path)
            if candidateVector is not None:
                score = cosine_similarity(targetVector.reshape(1, -1), candidateVector.reshape(1, -1))[0][0]
                similarity_scores.append((path, score))
        
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        return similarity_scores[:topN] 