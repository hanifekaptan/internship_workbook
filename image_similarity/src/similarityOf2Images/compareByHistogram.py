import cv2
import numpy as np
from PIL import Image

class HistogramBasedImageSimilarity:

    def _preprocessImage(self, imgPath):
        img = cv2.imread(imgPath)
        if img is None:
            print(f"Hata: Görüntü dosyası okunamadı veya bulunamadı: {imgPath}")
            return None
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    def _calculateHistogramAndNormalize(self, img):
        hist = cv2.calcHist([img], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        return hist


    def _compareHistograms(self, hist1, hist2, method=cv2.HISTCMP_CORREL):
        return cv2.compareHist(hist1, hist2, method)


    def calculateSimilarity(self, img1Path, img2Path, method=cv2.HISTCMP_CORREL):
        try:
            img1 = self._preprocessImage(img1Path)
            img2 = self._preprocessImage(img2Path)

            if img1 is None or img2 is None:
                return 0

            h, w, _ = img1.shape
            img2 = cv2.resize(img2, (w, h))

            hist1 = self._calculateHistogramAndNormalize(img1)
            hist2 = self._calculateHistogramAndNormalize(img2)

            score = self._compareHistograms(hist1, hist2, method)
            return score * 100

        except Exception as e:
            print(f"Beklenmedik bir hata oluştu: {e}")
            return 0
