# sonuçların tamamı 0'a yakın
# bu da ORB'nin benzerlik ölçümünün başarısız olduğunu gösterir.

import cv2
from PIL import Image
import numpy as np


class ORBBasedImageSimilarity:

    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=1000)

    def _readImage(self, imgPath):
        img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Error: Image file could not be read or found: {imgPath}")
            return None
        return img


    def _detectAndCompute(self, img):
        if img is None:
            print("Error: Image is None.")
            return None, None
        keypoints, descriptors = self.orb.detectAndCompute(img, None)
        return keypoints, descriptors

    
    def _matchDescriptors(self, descriptors1, descriptors2, goodMatchThreshold=0.7):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        allMatches = bf.knnMatch(descriptors1, descriptors2, k=2)
        goodMatches = []
        for matchGroup in allMatches:
            if len(matchGroup) < 2:
                continue
            m, n = matchGroup
            if m.distance < goodMatchThreshold * n.distance:
                goodMatches.append(m)   
        return goodMatches


    def calculateSimilarity(self, img1Path, img2Path, goodMatchThreshold=0.75):
        try:
            img1 = self._readImage(img1Path)
            img2 = self._readImage(img2Path)
            if img1 is None or img2 is None:
                return 0.0
            keypoints1, descriptors1 = self._detectAndCompute(img1)
            keypoints2, descriptors2 = self._detectAndCompute(img2)
            if descriptors1 is None or descriptors2 is None or len(keypoints1) == 0 or len(keypoints2) == 0:
                return 0.0
            goodMatches = self._matchDescriptors(descriptors1, descriptors2, goodMatchThreshold)
            similarity = (len(goodMatches) / max(len(keypoints1), len(keypoints2))) * 100
            return similarity
        except cv2.error as e:
            print(f"OpenCV (ORB) Hatası: {e}")
            return 0.0
        except Exception as e:
            print(f"Genel ORB Hatası: {e}")
            return 0.0
