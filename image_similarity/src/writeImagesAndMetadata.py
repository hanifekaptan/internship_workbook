import os
from pathlib import Path
from PIL import Image
from typing import List, Dict, Any
from src.utils.databaseManager import DatabaseManager

projectRoot = Path(__file__).resolve().parents[1]
dbFolder = projectRoot / "databases"
imageDataBaseFolder = projectRoot / "datasets"


class ImagePopulator:

    def _collectMetadataFromFolder(self, dataPath: Path) -> List[Dict[str, Any]]:
        if not dataPath.is_dir():
            print(f"-> Uyarı: Görüntü klasörü bulunamadı: '{dataPath}'.")
            return []
        
        imageMetadataList = []
        imageFiles = [f for f in os.listdir(dataPath) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"-> '{dataPath.name}' klasöründeki {len(imageFiles)} görüntü taranıyor...")
        for fileName in imageFiles:
            fullPath = dataPath / fileName

            try:
                with Image.open(fullPath) as img:
                    width, height = img.size
                filesize = fullPath.stat().st_size / 1024  # KB olarak hesaplanır
                
                imageMetadataList.append({
                    'filename': fileName,
                    'filepath': str(fullPath),
                    'width': width,
                    'height': height,
                    'filesize_kb': filesize
                })
            except Exception as e:
                print(f"-> Hata: '{fileName}' dosyası işlenemedi - {e}")
                
        return imageMetadataList


    def runForDataset(self, datasetName: str):
        dbPath = dbFolder / f"{datasetName}.db"
        dataPath = imageDataBaseFolder / datasetName
        
        dataToInsert = self._collectMetadataFromFolder(dataPath)
        
        if dataToInsert:
            dbManager = DatabaseManager(str(dbPath))
            dbManager.insertMany('images', dataToInsert)
