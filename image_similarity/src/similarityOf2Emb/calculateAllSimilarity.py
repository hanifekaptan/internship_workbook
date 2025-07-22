import sqlite3
import numpy as np
import faiss
import itertools
from pathlib import Path
from tqdm import tqdm
import time
import sys


class EmbeddingSimilarityCalculator:

    def calculateCosineSimilarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        if norm1 == 0 or norm2 == 0: return 0.0
        cosine_similarity = dot_product / (norm1 * norm2)
        return ((cosine_similarity + 1) / 2) * 100

    
    def calculateOklideanSimilarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        distance = np.linalg.norm(emb1 - emb2)
        similarity = 1 / (1 + distance)
        return similarity * 100


    def calculateOklideanSimilarityWithFaiss(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        d = emb1.shape[0]
        emb1 = emb1.reshape(1, d).astype('float32')
        emb2 = emb2.reshape(1, d).astype('float32')
        index = faiss.IndexFlatL2(d)
        index.add(emb1)
        D, _ = index.search(emb2, k=1)
        distance = np.sqrt(D[0][0])
        similarity = 1 / (1 + distance)
        return similarity * 100