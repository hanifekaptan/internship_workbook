from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity
import re
from src.utils.preprocess import extractTextFromPdf

class Doc2VecSimilarity:
    def __init__(self):
        self.documents = []
        self.pdfPaths = []
        self.model = None

    def addPdfToCorpus(self, pdfPath):
        text = extractTextFromPdf(pdfPath)
        if text:
            words = text.lower().split()
            self.documents.append(TaggedDocument(words=words, tags=[pdfPath]))
            self.pdfPaths.append(pdfPath)

    def buildDoc2VecModel(self, vectorSize=100, window=5, minCount=1, workers=4, epochs=20):
        if not self.documents:
            return
        
        self.model = Doc2Vec(self.documents, vector_size=vectorSize, window=window, min_count=minCount, workers=workers, epochs=epochs)
        
    def getSimilarity(self, pdfPath1, pdfPath2):
        if self.model is None:
            return None
        if pdfPath1 not in self.pdfPaths or pdfPath2 not in self.pdfPaths:
            return None

        try:
            vector1 = self.model.dv[pdfPath1].reshape(1, -1)
            vector2 = self.model.dv[pdfPath2].reshape(1, -1)
            similarity_score = cosine_similarity(vector1, vector2)[0][0]
            return similarity_score
        except KeyError:
            return None
        except Exception as e:
            print(f"Doc2Vec benzerliği hesaplanırken hata oluştu: {e}")
            return None

    def getMostSimilar(self, targetPdfPath, topN=5):
        if self.model is None:
            return []
        if targetPdfPath not in self.pdfPaths:
            return []

        try:
            targetVector = self.model.dv[targetPdfPath].reshape(1, -1)
            similarity_scores = []
            for path in self.pdfPaths:
                if path == targetPdfPath:
                    continue
                try:
                    candidateVector = self.model.dv[path].reshape(1, -1)
                    score = cosine_similarity(targetVector, candidateVector)[0][0]
                    similarity_scores.append((path, score))
                except KeyError:
                    continue
            
            similarity_scores.sort(key=lambda x: x[1], reverse=True)
            return similarity_scores[:topN]
        except Exception as e:
            return [] 