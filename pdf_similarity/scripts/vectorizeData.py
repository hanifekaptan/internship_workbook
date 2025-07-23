import os
from src.vectorizePdf import PdfVectorizer

def main():
    pdfDir = "arxiv_pdfs_from_api"
    outputDir = "pdf_vectors"

    if os.path.exists(outputDir):
        for file in os.listdir(outputDir):
            os.remove(os.path.join(outputDir, file))
        os.rmdir(outputDir)
    
    pdfFiles = [os.path.join(pdfDir, f) for f in os.listdir(pdfDir) if f.endswith('.pdf')]
    
    # import random
    # if len(pdfFiles) > 10:
    #     pdfFiles = random.sample(pdfFiles, 10) # Rastgele 10 PDF seç

    if not pdfFiles:
        return

    vectorizer = PdfVectorizer(outputDir=outputDir)
    for pdfFile in pdfFiles:
        vectorizer.addPdfToCorpus(pdfFile)
    
    vectorizer.vectorizeAllPdfs()


if __name__ == "__main__":
    main() 