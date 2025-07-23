import os
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from src.utils.preprocess import extractTextFromPdf

class PdfVectorizer:
    def __init__(self, outputDir="pdf_vectors"):
        self.outputDir = outputDir
        os.makedirs(self.outputDir, exist_ok=True)
        self.corpus = {}
        self.pdfPaths = []

        self.tfidfVectorizer = TfidfVectorizer()
        self.doc2vecModel = None
        self.word2vecModel = None
        self.semanticModel = None
        self.semanticModelName = 'all-MiniLM-L6-v2'

    def _loadSemanticModel(self):
        if self.semanticModel is None:
            try:
                self.semanticModel = SentenceTransformer(self.semanticModelName)
            except Exception as e:
                print(f"Hata: Semantic model yüklenirken bir sorun oluştu: {e}")
                self.semanticModel = None

    def addPdfToCorpus(self, pdfPath):
        text = extractTextFromPdf(pdfPath)
        if text:
            self.corpus[pdfPath] = text
            self.pdfPaths.append(pdfPath)

    def vectorizeAllPdfs(self):
        if not self.corpus:
            # print("Vektörleştirilecek PDF bulunamadı. Lütfen 'addPdfToCorpus' ile PDF ekleyin.")
            return

        texts = [self.corpus[path] for path in self.pdfPaths]
        tfidfMatrix = self.tfidfVectorizer.fit_transform(texts)
        for i, pdfPath in enumerate(self.pdfPaths):
            vector = tfidfMatrix.getrow(i).toarray()[0]
            self._saveVector(pdfPath, vector, "tfidf")

        documents = [TaggedDocument(words=self.corpus[path].lower().split(), tags=[path]) for path in self.pdfPaths]
        if documents:
            self.doc2vecModel = Doc2Vec(documents, vector_size=100, window=5, min_count=1, workers=4, epochs=20)
            for pdfPath in self.pdfPaths:
                try:
                    vector = self.doc2vecModel.dv[pdfPath]
                    self._saveVector(pdfPath, vector, "doc2vec")
                except KeyError:
                    print(f"Uyarı: Doc2Vec modeli için {pdfPath} etiketi bulunamadı, vektör kaydedilemiyor.")
        # else:
        #     print("Doc2Vec için döküman bulunamadı.")

        tokenizedCorpus = [self.corpus[path].lower().split() for path in self.pdfPaths]
        if tokenizedCorpus:
            self.word2vecModel = Word2Vec(tokenizedCorpus, vector_size=100, window=5, min_count=1, workers=4, epochs=10)
            for pdfPath in self.pdfPaths:
                text = self.corpus[pdfPath]
                tokens = text.lower().split()
                validVectors = []
                for word in tokens:
                    if word in self.word2vecModel.wv:
                        validVectors.append(self.word2vecModel.wv[word])
                if validVectors:
                    vector = np.mean(validVectors, axis=0)
                    self._saveVector(pdfPath, vector, "wordEmbedding")
                # else:
                #     print(f"Uyarı: Word Embedding için {pdfPath} dosyasında geçerli kelime vektörü bulunamadı.")
        # else:
        #     print("Word Embedding için token bulunamadı.")

        
        self._loadSemanticModel()
        if self.semanticModel:
            for pdfPath in self.pdfPaths:
                text = self.corpus[pdfPath]
                try:
                    embedding = self.semanticModel.encode(text)
                    self._saveVector(pdfPath, embedding, "semantic")
                except Exception as e:
                    print(f"Hata: Semantic vektör oluşturulurken sorun oluştu {pdfPath}: {e}")
        # else:
        #     print("Semantic model yüklenemedi, semantic vektörler oluşturulamıyor.")
        

        for pdfPath in self.pdfPaths:
            text = self.corpus[pdfPath]
            numbers = []
            for s in text.split():
                try:
                    num = float(s)
                    numbers.append(num)
                except ValueError:
                    continue
            
            if numbers:
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
                    self._saveVector(pdfPath, np.zeros(10), "table")
                else:
                    self._saveVector(pdfPath, vector, "table")
            else:
                self._saveVector(pdfPath, np.zeros(10), "table")
        
        


    def _saveVector(self, pdfPath, vector, method):
        baseName = os.path.basename(pdfPath)
        fileName = f"{os.path.splitext(baseName)[0]}_{method}.npz"
        outputPath = os.path.join(self.outputDir, fileName)
        np.savez_compressed(outputPath, vector=vector)


    def loadVector(self, pdfPath, method):
        baseName = os.path.basename(pdfPath)
        fileName = f"{os.path.splitext(baseName)[0]}_{method}.npz"
        filePath = os.path.join(self.outputDir, fileName)
        if os.path.exists(filePath):
            data = np.load(filePath)
            return data['vector']
        return None 