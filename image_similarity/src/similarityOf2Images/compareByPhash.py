import imagehash
from PIL import Image
import numpy as np

class PHashBasedImageSimilarity:

    def _calculateHash(self, imgPath):
        try:
            hash = imagehash.phash(Image.open(imgPath))
            return hash
        except Exception as e:
            print(f"pHash Hatası: {e}")
            return 0

    def _calculateDistance(self, hash1, hash2):
        return hash1 - hash2

    def calculateSimilarity(self, imgPath1, imgPath2):
        hash1 = self._calculateHash(imgPath1)
        hash2 = self._calculateHash(imgPath2)
        if hash1 is None or hash2 is None:
            return 0.0
        distance = self._calculateDistance(hash1, hash2)
        try:
            max_dist = len(hash1.hash) ** 2
            if max_dist == 0:
                return 100.0 if distance == 0 else 0.0
            similarity = (1 - distance / max_dist) * 100
            return similarity
        except Exception as e:
            print(f"Benzerlik skoru hesaplanırken hata: {e}")
            return 0.0