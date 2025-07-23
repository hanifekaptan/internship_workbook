import PyPDF2
import pdfplumber

def extractTextFromPdf(pdfPath):
    text = ""
    try:
        with open(pdfPath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        
        if not text.strip():
            with pdfplumber.open(pdfPath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
    except Exception as e:
        print(f"Hata: {pdfPath} dosyasından metin çıkarılamadı: {e}")
    return text 