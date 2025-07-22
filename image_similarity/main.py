from src.utils.databaseManager import DatabaseManager
from src.writeImagesAndMetadata import ImagePopulator
from src.similarityOf2Emb.calculateAllSimilarity import EmbeddingSimilarityCalculator

import os
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import faiss
import itertools
from tqdm import tqdm


def writeImagesAndMetadata(datasetNames):
    
    populator = ImagePopulator()
    for dataset in datasetNames:
        populator.runForDataset(dataset)
    print("Görüntü ve meta veriler başarıyla yazıldı.")

def _calculateAllScoresForEmb(sortedKeys: List[str], emb1: str, emb2: str):
    records = {}
    records['image1'] = sortedKeys[0]
    records['image2'] = sortedKeys[1]
    records['cosine_score'] = allSimilarityCalculatorWithEmb.calculateCosineSimilarity(emb1, emb2)
    records['oklidean_score'] = allSimilarityCalculatorWithEmb.calculateOklideanSimilarity(emb1, emb2)
    records['oklidean_with_faiss_score'] = allSimilarityCalculatorWithEmb.calculateOklideanSimilarityWithFaiss(emb1, emb2)
    return records

def writeEmbeddings(datasetName: str, embeddingFile: str):
    dbPath = str(DB_FOLDER / f"{datasetName}.db")
    dbManager = DatabaseManager(dbPath)

    data = np.load(embeddingFile)
    imageKeys = data.files
    embeddings = {key: data[key] for key in imageKeys}
    uniquePairs = list(itertools.combinations(imageKeys, 2))

    recordsToInsert = []
    for img1Key, img2Key in tqdm(uniquePairs, desc="Çiftler İşleniyor", unit=" çift"):
        emb1, emb2 = embeddings[img1Key], embeddings[img2Key]
        sortedKeys = sorted([img1Key, img2Key])
        records = _calculateAllScoresForEmb(sortedKeys, emb1, emb2)
        recordsToInsert.append(records)

    if recordsToInsert:
        dbManager.insertMany('similarities', recordsToInsert)

if __name__ == "__main__":
    
    PROJECT_ROOT = Path(__file__).resolve().parent
    DB_FOLDER = PROJECT_ROOT / "databases"
    DATASET_NAMES = ["wildlifeTiger"]
    writeImagesAndMetadata(DATASET_NAMES)

    allSimilarityCalculatorWithEmb = EmbeddingSimilarityCalculator()
    for dataset in DATASET_NAMES:
        embeddingFile = f"{dataset}Embeddings.npz"
        writeEmbeddings(dataset, embeddingFile)



