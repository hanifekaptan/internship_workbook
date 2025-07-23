import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

class VectorComparer:
    def getSimilarity(self, vector1, vector2):
        if vector1 is None or vector2 is None:
            return None

        if np.isnan(vector1).any() or np.isinf(vector1).any() or \
           np.isnan(vector2).any() or np.isinf(vector2).any():
            return None

        similarity_score = cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))[0][0]
        return float(similarity_score)

    def getMostSimilar(self, targetVector, candidateVectors, topN=5):
        if targetVector is None or not candidateVectors:
            return []
        
        if np.isnan(targetVector).any() or np.isinf(targetVector).any():
            return []

        similarity_scores = []
        for path, vec in candidateVectors.items():
            if vec is not None:
                if np.isnan(vec).any() or np.isinf(vec).any():
                    continue
                score = cosine_similarity(targetVector.reshape(1, -1), vec.reshape(1, -1))[0][0]
                similarity_scores.append((path, float(score)))

        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        return similarity_scores[:topN] 