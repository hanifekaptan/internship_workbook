# PDF Benzerlik Analizi

## 1. Anahtar Kelime Tabanlı Yaklaşım: `tfidfSimilarity.py`

### Ne İşe Yarar?
Bu yöntem, belgeler arasındaki benzerliği **TF-IDF (Term Frequency-Inverse Document Frequency)** metriğini kullanarak ölçer. TF-IDF, bir kelimenin bir belge içindeki ve tüm belge koleksiyonundaki (corpus) istatistiksel önemini ortaya koyar.

### Nasıl Çalışır?
1.  Her PDF dosyasından metin içeriği çıkarılır.
2.  Çıkarılan metinler, `TfidfVectorizer` kullanılarak sayısal TF-IDF vektörlerine dönüştürülür.
3.  İki belge arasındaki benzerlik, bu vektörler arasındaki **kosinüs benzerliği** (cosine similarity) hesaplanarak bulunur.

### Ayırt Edici Özelliği
> Bu yöntem, kelimelerin anlamsal anlamını değil, yalnızca istatistiksel önemini ve sıklığını dikkate alır. "Araba" ve "otomobil" kelimelerinin benzer anlam taşıdığını anlayamaz.

---

## 2. Bağlamsal Belge Vektörleri: `doc2vecSimilarity.py`

### Ne İşe Yarar?
Bu sınıf, **Doc2Vec** (veya Paragraf Vektörleri) modelini kullanarak tüm bir belgenin anlamsal bir temsilini oluşturur. Word2Vec'in bir uzantısı olarak, sadece kelimeleri değil, belgelerin bütününü vektörleştirir.

### Nasıl Çalışır?
1.  PDF'lerden metin çıkarılır ve ön işleme tabi tutulur.
2.  Her belge bir `TaggedDocument` nesnesine dönüştürülür.
3.  Bu etiketlenmiş belgeler kullanılarak bir Doc2Vec modeli eğitilir ve her belge için yoğun bir vektör (dense vector) oluşturulur.
4.  Benzerlik, bu belge vektörleri arasındaki kosinüs benzerliği ile hesaplanır.

### Ayırt Edici Özelliği
> TF-IDF'in aksine, Doc2Vec kelimelerin sırasını ve bağlamını dikkate alarak belgelerin anlamsal anlamını yakalamayı hedefler. Bu sayede daha derin bir içerik analizi sunar.

---

## 3. Kelime Gömüleri ile Benzerlik: `wordEmbeddingSimilarity.py`

### Ne İşe Yarar?
Bu yaklaşım, belge benzerliğini **Word2Vec** gibi kelime gömme (word embedding) modelleri aracılığıyla hesaplar. Bir belgenin temsilini, o belgedeki kelime vektörlerinin bir birleşimi (genellikle ortalaması) olarak oluşturur.

### Nasıl Çalışır?
1.  PDF metinleri çıkarılır ve kelimelere (token) ayrılır.
2.  Bu kelimeler üzerinde bir Word2Vec modeli eğitilerek her kelime için bir vektör oluşturulur.
3.  Bir belgenin genel vektörü, o belgedeki tüm kelime vektörlerinin **ortalaması** alınarak elde edilir.
4.  Belgeler arası benzerlik, bu ortalama vektörler üzerinden kosinüs benzerliği ile hesaplanır.

### Ayırt Edici Özelliği
> Bu yöntem, kelimelerin anlamsal ilişkilerini anlar ("kral" - "erkek" + "kadın" ≈ "kraliçe" gibi). Ancak, belge vektörünü basit bir ortalama ile oluşturduğu için Doc2Vec'e kıyasla cümle ve paragraf düzeyindeki bağlamsal bilgilerin bir kısmını kaybedebilir.

---

## 4. Gelişmiş Anlamsal Benzerlik: `semanticSimilarity.py`

### Ne İşe Yarar?
Bu sınıf, **Sentence Transformers** gibi önceden eğitilmiş, son teknoloji dil modellerini kullanarak belgeler arasında yüksek doğruluklu anlamsal benzerlik hesaplar.

### Nasıl Çalışır?
1.  PDF'ten metin çıkarılır.
2.  Önceden eğitilmiş bir model (örneğin, `'paraphrase-MiniLM-L6-v2'`) kullanılarak tüm metin, anlamsal olarak zengin tek bir gömüye (vektöre) dönüştürülür.
3.  Benzerlik, bu gelişmiş gömüler arasındaki kosinüs benzerliği ile ölçülür.

### Ayırt Edici Özelliği
> Diğer yöntemlerden farklı olarak, bu yaklaşım cümle ve belgeleri anlamsal olarak karşılaştırmak için özel olarak eğitilmiş modeller kullanır. Genellikle, metnin genel anlamını ve nüanslarını yakalamada en yüksek performansı gösterir.

---

## 5. Yapısal Veri Odaklı Yaklaşım: `tableSimilarity.py`

### Ne İşe Yarar?
Bu sınıf, diğerlerinden farklı olarak PDF'lerin metinsel içeriğine değil, içerdikleri **tablolar** gibi yapısal verilere odaklanır. Amacı, benzer yapılandırılmış bilgiye sahip belgeleri bulmaktır.

### Nasıl Çalışır?
1.  `pdfplumber` gibi bir kütüphane ile PDF dosyalarındaki tablolar tespit edilir ve çıkarılır.
2.  Çıkarılan tablo verileri metin formatına (örneğin CSV dizesi) dönüştürülür.
3.  Bu metinler, TF-IDF gibi bir yöntemle karşılaştırılarak tabloların benzerliği hesaplanır.

### Ayırt Edici Özelliği
> Bu yöntem, yalnızca belgenin belirli bir yapısal öğesine odaklanmasıyla benzersizdir. Genel metin analizinin gözden kaçırabileceği, yapılandırılmış verilerdeki (sayılar, istatistikler, listeler) benzerlikleri yakalamak için kritik öneme sahiptir.

---

## Yöntemlerin Karşılaştırmalı Özeti

| Dosya Adı | Temel Yaklaşım | Güçlü Yönü | Zayıf Yönü / Sınırlaması |
| :--- | :--- | :--- | :--- |
| **`tfidfSimilarity.py`** | Anahtar Kelime Sıklığı | Hızlı ve basittir. Aynı anahtar kelimeleri paylaşan belgeleri bulur. | Anlam ve bağlamı anlamaz. |
| **`doc2vecSimilarity.py`** | Belge Gömüleri | Kelime sırasını ve belge bağlamını dikkate alır. | Eğitim gerektirir ve büyük veri setlerinde daha iyi çalışır. |
| **`wordEmbeddingSimilarity.py`** | Kelime Gömüleri (Ortalama) | Kelimelerin anlamsal anlamını yakalar. | Belge bağlamını ortalama alarak basitleştirir. |
| **`semanticSimilarity.py`** | Gelişmiş Dil Modelleri | Anlamı ve nüansları en iyi şekilde yakalar. Çok yüksek doğruluk sunar. | Diğerlerine göre daha fazla hesaplama gücü gerektirebilir. |
| **`tableSimilarity.py`** | Yapısal Veri Analizi | Metin analizinin kaçıracağı tablo benzerliklerini bulur. | Yalnızca tablo içeriğini analiz eder, genel metni göz ardı eder. |
