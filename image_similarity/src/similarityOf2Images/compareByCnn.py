import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image as tfImage
from tensorflow.keras.applications.resnet50 import preprocess_input
from scipy.spatial import distance
from PIL import Image

class CNNBasedImageSimilarity:

    def __init__(self):
        try:
            self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        except Exception as e:
            print(f"Hata: CNN modeli yüklenemedi. Hata: {e}")
            self.model = None


    def _getFeatureVector(self, imgPath: str) -> np.ndarray:
        img = tfImage.load_img(imgPath, target_size=(224, 224))
        imgArray = tfImage.img_to_array(img)
        expandedImgArray = np.expand_dims(imgArray, axis=0)
        preprocessedImg = preprocess_input(expandedImgArray)
        features = self.model.predict(preprocessedImg, verbose=0)
        return features.flatten()


    def calculateSimilarity(self, imgPath1: str, imgPath2: str) -> float:
        if self.model is None:
            print("Hata: Model yüklenemediği için benzerlik hesaplanamıyor.")
            return 0.0

        try:
            vec1 = self._getFeatureVector(imgPath1)
            vec2 = self._getFeatureVector(imgPath2)
            cosineDistance = distance.cosine(vec1, vec2)
            similarityScore = (1 - cosineDistance) * 100
            return similarityScore
        
        except Exception as e:
            print(f"CNN Benzerlik Hatası: Görüntüler işlenirken bir sorun oluştu. Hata: {e}")
            return 0.0
