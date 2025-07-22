import os
import time
from pathlib import Path
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from tqdm import tqdm

def create_embeddings_from_folder(image_folder: Path, output_file: Path, model, processor, device: str):
    valid_extensions = ('.png', '.jpg', '.jpeg')
    image_paths = [p for p in image_folder.glob('*') if p.suffix.lower() in valid_extensions]
    if not image_paths:
        print(f"Hata: '{image_folder}' klasöründe işlenecek görsel bulunamadı.")
        return
    print(f"{len(image_paths)} adet görsel bulundu. Embedding işlemi başlıyor...")
    # overall_start_time = time.time()
    embeddings_data = {}
    for image_path in tqdm(image_paths, desc="Embedding'ler oluşturuluyor"):
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt", padding=True).to(device)
            with torch.no_grad():
                image_features = model.get_image_features(**inputs)
            embeddings_data[image_path.name] = image_features.cpu().numpy().flatten()
        except Exception as e:
            print(f"\nUyarı: {image_path.name} dosyası işlenemedi. Atlanıyor. Hata: {e}")
            continue
    # total_duration = time.time() - overall_start_time
    if not embeddings_data:
        print("Hiçbir görsel için embedding oluşturulamadı.")
        return

    try:
        np.savez_compressed(output_file, **embeddings_data)
        print("\n" + "="*50)
        print(" İŞLEM BAŞARIYLA TAMAMLANDI ".center(50, "="))
        print("="*50)
        print(f"Oluşturulan embedding sayısı: {len(embeddings_data)}")
        print(f"Toplam süre: {total_duration:.2f} saniye")
        print(f"Sonuçlar şuraya kaydedildi: '{output_file}'")
        print("="*50)
    except IOError as e:
        print(f"\nHata: Sonuçlar dosyaya yazılamadı. - {e}")

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    dataset_name = ["wildlifeTiger"]
    for dataset in dataset_name:
        print(f"\nİşlem başlatılıyor: '{dataset}'")
        TEST_IMAGES_FOLDER = PROJECT_ROOT / "datasets" / dataset
        OUTPUT_NPZ_FILE = PROJECT_ROOT / f"{dataset}Embeddings.npz"
        MODEL_NAME = "openai/clip-vit-base-patch32"
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Kullanılacak cihaz: {DEVICE.upper()}")
        if not TEST_IMAGES_FOLDER.is_dir():
            print(f"Hata: '{TEST_IMAGES_FOLDER}' adında bir klasör bulunamadı.")
        else:
            print(f"Model yükleniyor: '{MODEL_NAME}'... (Bu işlem biraz sürebilir)")
            model = CLIPModel.from_pretrained(MODEL_NAME).to(DEVICE)
            processor = CLIPProcessor.from_pretrained(MODEL_NAME)
            print("Model başarıyla yüklendi.")
            create_embeddings_from_folder(
                image_folder=TEST_IMAGES_FOLDER,
                output_file=OUTPUT_NPZ_FILE,
                model=model,
                processor=processor,
                device=DEVICE
            )