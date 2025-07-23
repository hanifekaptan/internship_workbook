import os
import pandas as pd
from src.vectorizePdf import PdfVectorizer
from src.compare2Emb.vectorComparer import VectorComparer

def main():
    pdfDir = "arxiv_pdfs_from_api"
    outputDir = "pdf_vectors"
    similarityResultCsv = "similarity_results_emb.csv"

    vectorizer = PdfVectorizer(outputDir=outputDir)

    vectorComparer = VectorComparer()

    pdfFiles = [os.path.join(pdfDir, f) for f in os.listdir(pdfDir) if f.endswith('.pdf')]
    if not pdfFiles:
        print(f"Uyarı: '{pdfDir}' dizininde PDF dosyası bulunamadı.")
        return

    allPdfVectors = {}
    for pdfFile in pdfFiles:
        docVectors = {
            "tfidf": vectorizer.loadVector(pdfFile, "tfidf"),
            "doc2vec": vectorizer.loadVector(pdfFile, "doc2vec"),
            "wordEmbedding": vectorizer.loadVector(pdfFile, "wordEmbedding"),
            "semantic": vectorizer.loadVector(pdfFile, "semantic"),
            "table": vectorizer.loadVector(pdfFile, "table"),
        }
        if all(v is not None for v in docVectors.values()):
            allPdfVectors[pdfFile] = docVectors
        else:
            print(f"Uyarı: {os.path.basename(pdfFile)} için tüm vektörler yüklenemedi, atlanıyor.")

    if len(allPdfVectors) < 2:
        # print("Uyarı: Benzerlik karşılaştırması için en az iki PDF vektör seti gereklidir.")
        return

    similarityScores = []
    pdfPathsList = list(allPdfVectors.keys())

    totalComparisons = (len(pdfPathsList) * (len(pdfPathsList) - 1)) // 2
    processedCount = 0

    for i in range(len(pdfPathsList)):
        for j in range(i + 1, len(pdfPathsList)):
            pdf1Path = pdfPathsList[i]
            pdf2Path = pdfPathsList[j]

            vec1 = allPdfVectors[pdf1Path]
            vec2 = allPdfVectors[pdf2Path]

            tfidfScore = vectorComparer.getSimilarity(vec1["tfidf"], vec2["tfidf"])
            doc2vecScore = vectorComparer.getSimilarity(vec1["doc2vec"], vec2["doc2vec"])
            wordEmbeddingScore = vectorComparer.getSimilarity(vec1["wordEmbedding"], vec2["wordEmbedding"])
            semanticScore = vectorComparer.getSimilarity(vec1["semantic"], vec2["semantic"])
            tableScore = vectorComparer.getSimilarity(vec1["table"], vec2["table"])

            similarityScores.append({
                "pdf1": os.path.basename(pdf1Path),
                "pdf2": os.path.basename(pdf2Path),
                "tfidfSimilarity": tfidfScore,
                "doc2vecSimilarity": doc2vecScore,
                "wordEmbeddingSimilarity": wordEmbeddingScore,
                "semanticSimilarity": semanticScore,
                "tableSimilarity": tableScore
            })
            processedCount += 1
            # if processedCount % 100 == 0:
            #     print(f"{processedCount}/{totalComparisons} karşılaştırma tamamlandı.")

    df = pd.DataFrame(similarityScores)
    df.to_csv(similarityResultCsv, index=False)
   
if __name__ == "__main__":
    main() 