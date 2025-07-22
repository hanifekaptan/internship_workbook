import cv2
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np

class SSIMBasedImageSimilarity:

    def _readImage(self, imgPath):
        img = cv2.imread(imgPath)
        if img is None:
            print(f"Hata: Görüntü dosyası okunamadı veya bulunamadı: {imgPath}")
            return None
        return img

    def _grayscaleResize(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def calculateSimilarity(self, img1Path, img2Path):
        img1 = self._readImage(img1Path)
        img2 = self._readImage(img2Path)
        if img1 is None or img2 is None:
            return 0
        try:
            h, w, _ = img1.shape
            img2 = cv2.resize(img2, (w, h))
            img1_gray = self._grayscaleResize(img1)
            img2_gray = self._grayscaleResize(img2)
            score, _ = ssim(img1_gray, img2_gray, full=True)
            return score * 100
        except Exception as e:
            print(f"SSIM Hatası: {e}")
            return 0