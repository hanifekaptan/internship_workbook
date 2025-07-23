import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# manuel olarak dosya yolu eklenmelidir
dosya_yolu = r'pdf_similarity\result\similarity_results_emb.csv'
df = pd.read_csv(dosya_yolu)

# print("Veri Setinin İlk 5 Satırı:")
# print(df.head())

# print("\nSayısal Sütunların İstatistiksel Özeti:")
# print(df.describe())

sns.set_theme(style="whitegrid")

# boxplot
plt.figure(figsize=(14, 8))
sns.boxplot(data=df.drop(['pdf1', 'pdf2'], axis=1))
plt.title('Farklı Benzerlik Algoritmalarının Skor Dağılımları', fontsize=16)
plt.ylabel('Benzerlik Skoru', fontsize=12)
plt.xlabel('Algoritmalar', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# heatmap
similarity_scores = df.drop(['pdf1', 'pdf2'], axis=1)
corr_matrix = similarity_scores.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Benzerlik Algoritmaları Arasındaki Korelasyon', fontsize=16)
plt.show()