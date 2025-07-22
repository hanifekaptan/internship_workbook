import PIL
import numpy as np
from PIL import Image


class PixelBasedImageSimilarity:

    def _openImg(self, imgPath):
        return Image.open(imgPath)


    def _convertToArray(self, img):
        return np.array(img).astype('float')

    
    def calculateSimilarity(self, img1Path, img2Path):
        try:
            img1 = self._openImg(img1Path)
            img2 = self._openImg(img2Path)
            img2 = img2.resize(img1.size)
            arr1 = self._convertToArray(img1)
            arr2 = self._convertToArray(img2)
            err = np.sum((arr1 - arr2) ** 2)
            err /= float(arr1.shape[0] * arr1.shape[1])
            similarity = max(0, 100 - (err / 100))
            return similarity

        except Exception as e:
            print(f"Piksel Hatası: {e}")
            return 0