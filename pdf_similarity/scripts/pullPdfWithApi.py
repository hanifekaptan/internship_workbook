import requests
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import time
import xml.etree.ElementTree as ET
import random


CATEGORIES_TO_SAMPLE = {
    'cs.CV': 100,
    'cs.AI': 100,
    'math.ST': 100,
    'physics.med-ph': 100,
    'q-bio.NC': 100
}

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_OUTPUT_FOLDER = PROJECT_ROOT / "arxiv_pdfs_from_api"

def get_paper_ids_from_category(category: str, num_samples: int) -> list:
    base_url = 'http://export.arxiv.org/api/query?'
    random_start_index = random.randint(0, 2000)
    
    params = {
        'search_query': f'cat:{category}',
        'start': random_start_index,
        'max_results': num_samples,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        paper_ids = []
        for entry in root.findall('atom:entry', namespace):
            full_id_url = entry.find('atom:id', namespace).text
            paper_id = full_id_url.split('/abs/')[-1].split('v')[0]
            paper_ids.append(paper_id)
            
        return paper_ids
    except requests.exceptions.RequestException as e:
        print(f"\nHATA: '{category}' kategorisi için API isteği başarısız oldu. Hata: {e}")
        return []

def download_pdf(arxiv_id: str, output_folder: Path):
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    file_path = output_folder / f"{arxiv_id}.pdf"
    
    if file_path.exists():
        return 'already_exists'
        
    try:
        response = requests.get(pdf_url, stream=True, timeout=15)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return 'downloaded'
    except requests.exceptions.RequestException:
        return 'failed'

if __name__ == "__main__":
    all_paper_ids_to_download = []
    
    for category, num_samples in CATEGORIES_TO_SAMPLE.items():
        ids = get_paper_ids_from_category(category, num_samples)
        all_paper_ids_to_download.extend(ids)
        time.sleep(2)
    unique_ids = sorted(list(set(all_paper_ids_to_download)))
    total_to_download = len(unique_ids)
    PDF_OUTPUT_FOLDER.mkdir(exist_ok=True)
    downloaded_count = 0
    failed_count = 0
    with tqdm(total=total_to_download, desc="PDF'ler İndiriliyor") as pbar:
        for arxiv_id in unique_ids:
            status = download_pdf(arxiv_id, PDF_OUTPUT_FOLDER)
            if status == 'downloaded':
                downloaded_count += 1
            elif status == 'failed':
                failed_count += 1
            pbar.update(1)
            if status == 'downloaded':
                time.sleep(1) 

    print("\n--- İŞLEM TAMAMLANDI ---")
    print(f"Başarıyla indirilen PDF sayısı: {downloaded_count}")
    print(f"Atlanan (zaten mevcuttu): {total_to_download - downloaded_count - failed_count}")
    print(f"Başarısız olan indirme sayısı: {failed_count}")