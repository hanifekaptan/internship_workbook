"""
OUTPUT:
Görüntü dosyaları organize ediliyor.
Kaynak klasör: e:\Ben\bt10\week2\original-datasets
Hedef klasör: e:\Ben\bt10\week2\datasets
------------------------------
'wildlife-tiger' kategorisi işleniyor...
-> 'wildlife-tiger' kategorisi için toplam 2762 görüntü dosyası 'e:\Ben\bt10\week2\datasets\wildlife-tiger' klasörüne kopyalandı.
------------------------------
Görüntü dosyaları organize edildi..
"""


import os
import shutil
from pathlib import Path

print("Görüntü dosyaları organize ediliyor.")

projectRoot = Path(__file__).parent.parent
sourceBaseDir = projectRoot / "original-datasets"
targetBaseDir = projectRoot / "datasets"
imageExtensions = {".jpg", ".jpeg", ".png"}

if not sourceBaseDir.is_dir():
    print(f"HATA: Kaynak klasör bulunamadı: {sourceBaseDir}")
    exit()

targetBaseDir.mkdir(exist_ok=True)
print(f"Kaynak klasör: {sourceBaseDir}")
print(f"Hedef klasör: {targetBaseDir}")
print("-" * 30)

for categoryDir in sourceBaseDir.iterdir():
    if categoryDir.is_dir():
        categoryName = categoryDir.name
        print(f"'{categoryName}' kategorisi işleniyor...")

        targetCategoryPath = targetBaseDir / categoryName
        targetCategoryPath.mkdir(exist_ok=True)

        copiedCount = 0
        for sourceFilePath in categoryDir.rglob('*'):
            if sourceFilePath.is_file() and sourceFilePath.suffix.lower() in imageExtensions:
                
                targetFilePath = targetCategoryPath / sourceFilePath.name

                shutil.copy2(sourceFilePath, targetFilePath)
                copiedCount += 1
        
        print(f"-> '{categoryName}' kategorisi için toplam {copiedCount} görüntü dosyası '{targetCategoryPath}' klasörüne kopyalandı.")

print("-" * 30)
print("Görüntü dosyaları organize edildi.")