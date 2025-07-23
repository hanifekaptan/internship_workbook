import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.preprocess import extractTextFromPdf
import os

class TableSimilarity:
    def __init__(self):
        self.corpus = {}
        self.pdfPaths = []
        self.tableVectors = {}

    def addPdfToCorpus(self, pdfPath):
        text = extractTextFromPdf(pdfPath)
        if text:
            self.corpus[pdfPath] = text
            self.pdfPaths.append(pdfPath)
    
    def _extractAndVectorizeTables(self, pdfPath):
        text = self.corpus.get(pdfPath)
        if not text:
            return None

        numbers = []
        for s in text.split():
            try:
                num = float(s)
                numbers.append(num)
            except ValueError:
                continue
        
        if not numbers:
            return np.zeros(10)

        if len(numbers) == 1:
            vector = np.array([
                numbers[0],
                0.0,
                numbers[0],
                numbers[0],
                numbers[0], 0.0, 0.0, 0.0, 0.0,
            ])
            vector = np.pad(vector, (0, 10 - len(vector)), 'constant')
        elif len(numbers) < 5:
            vector = np.array([
                np.mean(numbers),
                np.std(numbers),
                np.min(numbers),
                np.max(numbers),
            ])
            vector = np.pad(vector, (0, 10 - len(vector)), 'constant')
        else:
            vector = np.array([
                np.mean(numbers),
                np.std(numbers),
                np.min(numbers),
                np.max(numbers),
                numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], 
            ])
        
        vector = np.pad(vector, (0, 10 - len(vector)), 'constant')

        if np.isnan(vector).any() or np.isinf(vector).any():
            return np.zeros(10)

        return vector

    def buildModel(self):
        for pdfPath in self.pdfPaths:
            self.tableVectors[pdfPath] = self._extractAndVectorizeTables(pdfPath)

    def getSimilarity(self, pdfPath1, pdfPath2):
        if pdfPath1 not in self.corpus or pdfPath2 not in self.corpus:
            return None

        vec1 = self.tableVectors.get(pdfPath1)
        vec2 = self.tableVectors.get(pdfPath2)

        if vec1 is None or vec2 is None:
            return None

        similarity_score = cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
        return similarity_score

    def getMostSimilar(self, targetPdfPath, topN=5):
        if targetPdfPath not in self.corpus:
            return []
        
        targetVector = self.tableVectors.get(targetPdfPath)
        if targetVector is None:
            return []

        similarity_scores = []
        for path in self.pdfPaths:
            if path == targetPdfPath:
                continue
            candidateVector = self.tableVectors.get(path)
            if candidateVector is not None:
                score = cosine_similarity(targetVector.reshape(1, -1), candidateVector.reshape(1, -1))[0][0]
                similarity_scores.append((path, score))
        
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        return similarity_scores[:topN] 