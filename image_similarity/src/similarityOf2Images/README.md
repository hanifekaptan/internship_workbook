## Görüntü Benzerliği Tespit Yöntemleri

Bu doküman, iki veya daha fazla görüntü arasındaki görsel benzerliği ölçmek için kullanılan çeşitli popüler ve etkili yöntemleri incelemektedir. Her bir yöntemin temel mantığı, avantajları, dezavantajları ve pratik uygulama alanları Python kod örnekleriyle birlikte sunulmuştur. Yöntemler, basit piksel karşılaştırmalarından karmaşık derin öğrenme modellerine kadar geniş bir yelpazeyi kapsamaktadır.

---

### 1. Histogram Bazlı Benzerlik (OpenCV ile)

Görüntü histogramı, bir görüntüdeki her bir renk tonunun piksel yoğunluğunu gösteren bir grafiktir. Başka bir deyişle, görüntüdeki renklerin dağılımını temsil eder. Histogram bazlı benzerlik, iki görüntünün renk paletlerinin ne kadar benzediğini ölçer. Bu yöntem, görüntüdeki nesnelerin konumu, yönü veya boyutuyla ilgilenmez; yalnızca genel renk kompozisyonuna odaklanır. Bu özelliği, onu döndürülmüş veya farklı şekilde kadrajlanmış ancak aynı renk temasına sahip görüntüleri bulmak için kullanışlı kılar.

Bu yöntemin en büyük avantajı hızı ve basitliğidir. Ancak önemli bir zayıflığı vardır: tamamen farklı konuları içeren iki görüntü, eğer benzer renk dağılımlarına sahiplerse (örneğin, bir gün batımı fotoğrafı ile turuncu ve sarı tonlarda soyut bir tablo) yüksek benzerlik skorları verebilirler. OpenCV, histogramları hesaplamak ve `cv2.compareHist` fonksiyonuyla aralarındaki korelasyon, ki-kare mesafesi gibi farklı metrikleri kullanarak karşılaştırmak için optimize edilmiş araçlar sunar.

**Örnek Kod:**

```python
import cv2
import numpy as np

def compare_images_by_histogram(img1_path, img2_path):
    # Görüntüleri oku ve HSV renk uzayına çevir (renk karşılaştırması için daha kararlıdır)
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    # Görüntüleri karşılaştırma için aynı boyuta getirelim
    h, w, _ = img1.shape
    img2 = cv2.resize(img2, (w, h))

    # Her iki görüntü için de histogramları hesapla
    # Hue (renk tonu) ve Saturation (doygunluk) kanallarını kullanacağız
    hist_img1 = cv2.calcHist([img1_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    hist_img2 = cv2.calcHist([img2_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

    # Histogramları normalize et (farklı boyutlardaki görüntüler için karşılaştırmayı adil hale getirir)
    cv2.normalize(hist_img1, hist_img1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist_img2, hist_img2, 0, 1, cv2.NORM_MINMAX)

    # Histogramları karşılaştır (Korelasyon metodu: 1'e ne kadar yakınsa o kadar benzer)
    similarity = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
    
    print(f"Histogram Benzerlik Skoru (Korelasyon): {similarity:.4f}")
    return similarity

# Örnek kullanım:
# compare_images_by_histogram('image1.jpg', 'image2.jpg')
```

---

### 2. Algısal Hashing (Perceptual Hashing) ile Benzerlik

Algısal hashing, bir görüntünün içeriğini analiz ederek sabit uzunlukta ve benzersiz bir "dijital parmak izi" (hash) oluşturma sürecidir. Kriptografik hash'lerin (MD5, SHA gibi) aksine, algısal hash'ler görüntüdeki küçük değişikliklere karşı toleranslıdır. Görüntünün yeniden boyutlandırılması, sıkıştırılması, parlaklığının değişmesi veya üzerine küçük bir filigran eklenmesi gibi durumlarda hash değeri çok az değişir veya hiç değişmez. Bu özellik, onu "neredeyse aynı" olan kopya görüntüleri bulmak için son derece etkili bir yöntem yapar.

`imagehash` gibi kütüphaneler bu işlemi çok basitleştirir. `aHash` (ortalama hash), `pHash` (algısal hash) ve `dHash` (fark hash'i) gibi çeşitli algoritmalar sunar. Bu algoritmalar, görüntüyü küçültüp basitleştirerek temel yapısal özelliklerini bir hash değerine sıkıştırır. İki görüntünün hash'i arasındaki Hamming mesafesi (bir sonraki bölümde açıklanmıştır) hesaplanarak aralarındaki benzerlik ölçülür. Bu yöntem, milyonlarca görüntülük devasa veritabanlarında bile kopya tespiti için olağanüstü hızlıdır.

**Örnek Kod:**

```python
from PIL import Image
import imagehash

def compare_images_by_phash(img1_path, img2_path):
    # Görüntüleri aç
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # Her iki görüntü için algısal hash (pHash) oluştur
    hash1 = imagehash.phash(img1)
    hash2 = imagehash.phash(img2)
    
    # Hash'ler arasındaki Hamming mesafesini hesapla
    # Mesafe ne kadar küçükse, görüntüler o kadar benzerdir. 0 mükemmel eşleşmedir.
    distance = hash1 - hash2
    
    # Mesafeyi 0-100 arası bir benzerlik skoruna çevirelim
    max_distance = len(hash1.hash) * len(hash1.hash[0]) # Genellikle 64
    similarity = (1 - distance / max_distance) * 100
    
    print(f"pHash Değeri 1: {hash1}")
    print(f"pHash Değeri 2: {hash2}")
    print(f"Hash'ler Arası Hamming Mesafesi: {distance}")
    print(f"Algısal Hash Benzerlik Skoru: {similarity:.2f}%")
    return similarity

# Örnek kullanım:
# compare_images_by_phash('image1.jpg', 'image1_compressed.jpg')
```

---

### 3. Yapısal Benzerlik İndeksi (SSIM)

Yapısal Benzerlik İndeksi (SSIM), insan görsel sisteminin algıladığı görüntü kalitesi farklılıklarını ölçmek için tasarlanmış bir yöntemdir. Piksel veya histogram tabanlı yöntemlerin aksine SSIM, görüntüleri üç temel kritere göre karşılaştırır: **parlaklık (luminance)**, **kontrast (contrast)** ve **yapı (structure)**. Bu, onu iki görüntü arasındaki sıkıştırma kaynaklı bozulmaları, bulanıklığı veya gürültü gibi ince farkları tespit etmede çok güçlü kılar.

SSIM, genellikle bir orijinal görüntü ile onun işlenmiş veya sıkıştırılmış bir versiyonunu karşılaştırmak için kullanılır. Örneğin, bir video akışının kalitesini ölçmek veya bir fotoğraf düzenleme filtresinin etkisini değerlendirmek için idealdir. Tamamen farklı iki nesnenin fotoğrafını karşılaştırmak için tasarlanmamıştır. Sonuç -1 ile 1 arasında bir değerdir; 1 mükemmel benzerliği ifade eder. `scikit-image` ve `OpenCV` kütüphaneleri, SSIM hesaplaması için hazır ve optimize edilmiş fonksiyonlar sunar.

**Örnek Kod:**
(scikit-image kütüphanesi ile daha yaygın ve basittir.)

```python
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np

def compare_images_by_ssim(img1_path, img2_path):
    # Görüntüleri oku
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    # SSIM için görüntülerin aynı boyutta olması gerekir
    h, w, _ = img1.shape
    img2 = cv2.resize(img2, (w, h))

    # Karşılaştırma için görüntüleri gri tonlamaya çevir
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # SSIM skorunu hesapla
    # data_range, piksel değer aralığını belirtir.
    (score, diff) = ssim(img1_gray, img2_gray, full=True)
    
    print(f"Yapısal Benzerlik (SSIM) Skoru: {score:.4f}")
    return score

# Örnek kullanım:
# compare_images_by_ssim('original_photo.png', 'compressed_photo.jpg')
```

---

### 4. Özellik Eşleştirme (ORB ile Referans Görüntü Karşılaştırma)

Özellik eşleştirme, görüntülerdeki "ilginç" veya ayırt edici noktaları (köşeler, kenarlar, lekeler gibi) bularak çalışan çok güçlü bir tekniktir. ORB (Oriented FAST and Rotated BRIEF), bu özellikleri bulmak için kullanılan hızlı ve patent sorunu olmayan bir algoritmadır. Yöntem şu şekilde işler: Her iki görüntüde de binlerce anahtar nokta (keypoint) tespit edilir. Ardından, her bir anahtar noktanın etrafındaki bölge için o noktayı benzersiz kılan bir "tanımlayıcı" (descriptor) vektör oluşturulur. Son olarak, bir görüntüdeki tanımlayıcılar ile diğer görüntüdeki tanımlayıcılar karşılaştırılarak en iyi eşleşmeler bulunur.

Bu yöntemin en büyük gücü, görüntüdeki nesnenin ölçeğine, dönüşüne, aydınlatma koşullarına ve hatta kısmen kapanmasına (occlusion) karşı son derece dayanıklı olmasıdır. Bir görüntüdeki belirli bir nesnenin (örneğin bir kitap kapağının veya bir logunun), başka bir görüntüde farklı bir açıdan ve boyutta var olup olmadığını tespit etmek için mükemmeldir. İyi eşleşmelerin sayısı, iki görüntü arasındaki benzerliğin bir ölçüsü olarak kullanılabilir.

**Örnek Kod:**

```python
import cv2
import numpy as np

def compare_images_by_orb(img1_path, img2_path, good_match_threshold=0.7):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    # ORB dedektörünü başlat
    orb = cv2.ORB_create(nfeatures=2000) # nfeatures ile bulunacak özellik sayısı ayarlanabilir

    # Anahtar noktaları ve tanımlayıcıları bul
    keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

    # Brute-Force eşleştiriciyi oluştur
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    
    # Tanımlayıcıları eşleştir
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Lowe's Ratio Test ile iyi eşleşmeleri filtrele
    good_matches = []
    for m, n in matches:
        if m.distance < good_match_threshold * n.distance:
            good_matches.append(m)
    
    # Benzerlik skoru, toplam anahtar noktasına oranla iyi eşleşmelerin sayısı olabilir
    similarity = len(good_matches) / max(len(keypoints1), len(keypoints2)) * 100

    print(f"Toplam Eşleşme: {len(matches)}, İyi Eşleşme: {len(good_matches)}")
    print(f"Özellik Eşleştirme (ORB) Benzerlik Skoru: {similarity:.2f}%")
    return similarity

# Örnek kullanım:
# compare_images_by_orb('logo.png', 'photo_with_logo.jpg')
```
---

### 5. Derin Öğrenme Yöntemleri (CNN / Siyam Ağları)

Derin öğrenme, özellikle Evrişimli Sinir Ağları (CNN), görüntü benzerliği konusunda en gelişmiş ve en doğru sonuçları veren yöntemdir. Diğer yöntemlerin aksine, CNN'ler görüntüdeki özellikleri (kenarlar, dokular vb.) manuel olarak tanımlanmış kurallarla değil, milyonlarca görüntüden oluşan bir veri seti üzerinde eğitilerek "öğrenir". Bu sayede bir görüntünün anlamsal (semantik) içeriğini anlayabilirler. Örneğin, bir fotoğraftaki kedi ile bir çizgi filmdeki kedinin, insan için olduğu gibi model için de benzer olduğunu anlayabilirler.

Bu amaçla genellikle **Siyam Ağları (Siamese Networks)** kullanılır. Bu mimari, iki veya daha fazla özdeş CNN'den oluşur. Karşılaştırılacak görüntüler bu ağlara verilir ve her görüntü için bir "özellik vektörü" (embedding) çıktısı alınır. Bu vektör, görüntünün anlamsal özünü temsil eden çok boyutlu bir sayı dizisidir. Son olarak, bu iki vektör arasındaki mesafe (genellikle Kosinüs Benzerliği veya Öklid Mesafesi ile) hesaplanır. Mesafe ne kadar küçükse, görüntüler anlamsal olarak o kadar benzerdir. Bu yöntem çok güçlü olmasına rağmen, eğitilmesi için büyük veri setleri ve ciddi hesaplama gücü gerektirir.

**Örnek Kod (Kavramsal - Önceden Eğitilmiş Model Kullanımı):**

```python
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
from scipy.spatial import distance

def get_feature_vector(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    features = model.predict(preprocessed_img)
    return features.flatten()

def compare_images_by_cnn(img1_path, img2_path):
    # ImageNet üzerinde eğitilmiş ResNet50 modelini yükle (son sınıflandırma katmanı olmadan)
    base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    
    # Her iki görüntü için özellik vektörlerini çıkar
    vec1 = get_feature_vector(img1_path, base_model)
    vec2 = get_feature_vector(img2_path, base_model)

    # Vektörler arasındaki kosinüs mesafesini hesapla (0'a yakınsa benzer)
    cosine_distance = distance.cosine(vec1, vec2)
    
    # Mesafeyi 0-100 arası benzerlik skoruna çevir
    similarity = (1 - cosine_distance) * 100

    print(f"Vektörler Arası Kosinüs Mesafesi: {cosine_distance:.4f}")
    print(f"Derin Öğrenme (CNN) Benzerlik Skoru: {similarity:.2f}%")
    return similarity

# Örnek kullanım:
# compare_images_by_cnn('photo_of_a_car.jpg', 'another_photo_of_a_car.jpg')
```

---

### 6. Piksel Bazlı Karşılaştırma (Pillow ile)

Bu, görüntüleri karşılaştırmanın en temel ve en basit yöntemidir. İki görüntünün aynı koordinattaki (x, y) piksellerinin renk değerlerini (RGB) doğrudan birbiriyle karşılaştırır. Karşılaştırma genellikle iki görüntü arasındaki Ortalama Kare Hata (Mean Squared Error - MSE) veya Mutlak Hata Toplamı (Sum of Absolute Differences) hesaplanarak yapılır. Eğer iki görüntü bit-bit aynıysa, hata skoru sıfır olur. Bu yöntem çok hızlıdır ve uygulanması kolaydır.

Ancak bu yöntemin pratik kullanımı neredeyse yoktur. Görüntülerdeki en ufak bir değişiklik bile (örneğin, görüntünün bir piksel sağa kaydırılması, parlaklığının %1 değiştirilmesi veya farklı bir formatta kaydedilmesi) çok yüksek bir hata skoru üretir. Bu nedenle, yalnızca iki dosyanın dijital olarak birebir aynı olup olmadığını kontrol etmek gibi çok kısıtlı senaryolarda işe yarar. Gerçek dünyadaki görsel benzerlik tespiti için tamamen yetersizdir.

**Örnek Kod:**

```python
from PIL import Image
import numpy as np

def compare_images_by_pixel(img1_path, img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # Görüntülerin aynı modda ve boyutta olduğundan emin ol
    if img1.mode != img2.mode or img1.size != img2.size:
        print("Uyarı: Görüntüler farklı modda veya boyutta. Karşılaştırma anlamsız olabilir.")
        # Karşılaştırma için birini diğerinin formatına dönüştürelim
        img2 = img2.convert(img1.mode)
        img2 = img2.resize(img1.size)

    # Görüntüleri NumPy dizilerine çevir
    arr1 = np.array(img1).astype('float')
    arr2 = np.array(img2).astype('float')

    # Ortalama Kare Hatayı (MSE) hesapla. 0 mükemmel eşleşmedir.
    err = np.sum((arr1 - arr2) ** 2)
    err /= float(arr1.shape[0] * arr1.shape[1])
    
    print(f"Piksel Bazlı Ortalama Kare Hata (MSE): {err:.2f}")
    return err

# Örnek kullanım:
# compare_images_by_pixel('image1.png', 'image1_copy.png')
```
---

### 7. Hamming Mesafesi

Hamming mesafesi, kendi başına bir görüntü benzerlik yöntemi değil, bir **metriktir**. Özellikle Algısal Hashing gibi yöntemlerin bir parçası olarak kullanılır. Tanım olarak, eşit uzunluktaki iki karakter dizisi (genellikle binary) arasındaki Hamming mesafesi, bu dizilerin karşılıklı pozisyonlarında kaç tane farklı karakter olduğunu sayar. Örneğin, `101110` ve `100100` binary dizileri arasındaki mesafe 2'dir, çünkü 3. ve 5. pozisyonlardaki bitler farklıdır.

Algısal Hashing bağlamında, her görüntü bir hash dizisine (örneğin 64-bit'lik bir diziye) dönüştürülür. İki görüntünün benzerliğini ölçmek için bu iki hash dizisi arasındaki Hamming mesafesi hesaplanır. Mesafe '0' ise, bu iki görüntünün algısal olarak aynı olduğu kabul edilir. Mesafe arttıkça, görüntülerin birbirinden farklı olduğu anlaşılır. Bu metrik, hash tabanlı karşılaştırmaları son derece hızlı ve verimli hale getiren temel unsurdur.

**Örnek Kod (Kavramsal Gösterim - 2. Yöntemle Bütünleşik):**

```python
from PIL import Image
import imagehash

# Hamming Mesafesi, imagehash gibi kütüphaneler tarafından arka planda kullanılır.
# İşte bu kullanımın net bir gösterimi:

img1 = Image.open('image1.jpg')
img2 = Image.open('image2.jpg')

# Hash'leri oluştur
hash1 = imagehash.phash(img1)
hash2 = imagehash.phash(img2)

# İki hash objesini birbirinden çıkarmak, doğrudan aralarındaki Hamming mesafesini verir.
# Bu, imagehash kütüphanesinin sağladığı bir kolaylıktır.
hamming_distance = hash1 - hash2

print(f"Hash 1: {hash1}")
print(f"Hash 2: {hash2}")
print(f"İki hash arasındaki Hamming Mesafesi: {hamming_distance}")

# Mesafe 5'ten küçükse genellikle çok benzer kabul edilir.
if hamming_distance < 5:
    print("Görüntüler çok benzer.")
else:
    print("Görüntüler farklı.")
```