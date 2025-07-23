import os
import pandas as pd
from src.utils.preprocess import extractTextFromPdf
from src.compare2Pdf.doc2VecSimilarity import Doc2VecSimilarity
from src.compare2Pdf.semanticSimilarity import SemanticSimilarity
from src.compare2Pdf.tableSimilarity import TableSimilarity
from src.compare2Pdf.tfIdfSimilarity import TfidfSimilarity
from src.compare2Pdf.wordEmbeddingSimilarity import WordEmbeddingSimilarity

def process_pdf_pair(pdf1Path, pdf2Path, pdf_texts):
    """
    İki PDF arasındaki benzerlik skorlarını hesaplayan fonksiyon.
    Artık argümanları doğrudan alıyor.
    """
    semanticSim = SemanticSimilarity()
    text1 = pdf_texts.get(pdf1Path)
    text2 = pdf_texts.get(pdf2Path)

    if not text1 or not text2:
        print(f"Uyarı: {os.path.basename(pdf1Path)} veya {os.path.basename(pdf2Path)} için metin bulunamadı. Bu çift atlanıyor.")
        return None

    tfidfSim = TfidfSimilarity()
    tfidfSim.addPdfToCorpus(pdf1Path)
    tfidfSim.addPdfToCorpus(pdf2Path)
    tfidfSim.buildTfidfModel()

    doc2VecSim = Doc2VecSimilarity()
    doc2VecSim.addPdfToCorpus(pdf1Path)
    doc2VecSim.addPdfToCorpus(pdf2Path)
    doc2VecSim.buildDoc2VecModel()

    wordEmbeddingSim = WordEmbeddingSimilarity()
    wordEmbeddingSim.addPdfToCorpus(pdf1Path)
    wordEmbeddingSim.addPdfToCorpus(pdf2Path)
    wordEmbeddingSim.buildWordEmbeddingModel()

    semanticSim.addPdfToCorpus(pdf1Path)
    semanticSim.addPdfToCorpus(pdf2Path)

    tableSim = TableSimilarity()
    tableSim.addPdfToCorpus(pdf1Path)
    tableSim.addPdfToCorpus(pdf2Path)
    tableSim.buildModel()

    tfidfScore = tfidfSim.getSimilarity(pdf1Path, pdf2Path)
    doc2vecScore = doc2VecSim.getSimilarity(pdf1Path, pdf2Path)
    wordEmbeddingScore = wordEmbeddingSim.getSimilarity(pdf1Path, pdf2Path)
    semanticScore = semanticSim.getSimilarity(pdf1Path, pdf2Path)
    tableScore = tableSim.getSimilarity(pdf1Path, pdf2Path)

    return {
        "pdf1": os.path.basename(pdf1Path),
        "pdf2": os.path.basename(pdf2Path),
        "tfidfSimilarity": float(tfidfScore) if tfidfScore is not None else None,
        "doc2vecSimilarity": float(doc2vecScore) if doc2vecScore is not None else None,
        "wordEmbeddingSimilarity": float(wordEmbeddingScore) if wordEmbeddingScore is not None else None,
        "semanticSimilarity": float(semanticScore) if semanticScore is not None else None,
        "tableSimilarity": float(tableScore) if tableScore is not None else None
    }

def main():
    pdfDir = "arxiv_pdfs_from_api"
    pdfFiles = [os.path.join(pdfDir, f) for f in os.listdir(pdfDir) if f.endswith('.pdf')]
    
    # import random
    # if len(pdfFiles) > 10:
    #     pdfFiles = random.sample(pdfFiles, 10)
    
    if not pdfFiles:
        print(f"Uyarı: '{pdfDir}' dizininde işlenecek PDF dosyası bulunamadı.")
        return

    pdf_texts = {}
    for pdfFile in pdfFiles:
        text = extractTextFromPdf(pdfFile)
        if text:
            pdf_texts[pdfFile] = text

    pdfPairs = []
    for i in range(len(pdfFiles)):
        for j in range(i + 1, len(pdfFiles)):
            pdfPairs.append((pdfFiles[i], pdfFiles[j]))

    if not pdfPairs:
        print("Uyarı: Benzerlik karşılaştırması için yeterli PDF çifti bulunamadı.")
        return

    allSimilarityScores = []
    totalComparisons = len(pdfPairs)
    
    for i, (pdf1, pdf2) in enumerate(pdfPairs):
        result = process_pdf_pair(pdf1, pdf2, pdf_texts)
        if result:
            allSimilarityScores.append(result)
        
        if (i + 1) % 10 == 0:
            print(f"{i + 1}/{totalComparisons} karşılaştırma tamamlandı.")

    if allSimilarityScores:
        df = pd.DataFrame(allSimilarityScores)
        outputCsvPath = "similarity_results_pdf.csv"
        df.to_csv(outputCsvPath, index=False)
    else:
        print("Hiç benzerlik skoru hesaplanamadı.")


if __name__ == "__main__":
    main()