# 🧠 Kampüs AI - Akıllı Etkinlik & Bilgi Grafiği Sistemi (YM341)

> **Yapay Zeka Destekli, Graph-Tabanlı ve Konteynerize Edilmiş Etkinlik Yönetim Platformu**

Bu proje, geleneksel veritabanı sorgularının ötesine geçerek, **NLP (Doğal Dil İşleme)** ve **Graph Theory (Çizge Teorisi)** kullanarak etkinlikler arasındaki anlamsal ilişkileri analiz eden yeni nesil bir yönetim sistemidir.

![Graph View](./backend/static/graph-preview.png)
*(Buraya Graph ekran görüntünü ekleyebilirsin)*

## 🚀 Projenin Teknik Derinliği (Key Engineering Features)

Bu sistem sadece CRUD işlemleri yapan bir web sitesi değildir. Arka planda çalışan ileri seviye mühendislik çözümleri şunlardır:

### 1. 🕸️ Dinamik Bilgi Grafiği (Dynamic Knowledge Graph Construction)
* **Teknoloji:** `NetworkX` ve `Vis.js`
* **Mantık:** Sistemdeki her etkinlik bir "Düğüm" (Node) olarak kabul edilir. İçerik benzerlikleri hesaplanarak düğümler arası "Kenarlar" (Edges) matematiksel olarak oluşturulur.
* **Görselleştirme:** Veriler statik değil, **Physics Engine (Fizik Motoru)** destekli interaktif bir ağ haritası üzerinde sunulur.

### 2. 🧠 Semantik Arama Motoru (Semantic Vector Search)
* **Teknoloji:** `Sentence-Transformers (BERT)`, `Cosine Similarity`
* **Farkı:** Klasik "Kelime Bazlı" (Keyword) arama yerine, kullanıcının niyetini anlayan vektör tabanlı arama yapar.
* **Örnek:** "Keman" aratıldığında, içinde keman geçmese bile "Beethoven Gecesi"ni bulur çünkü anlamsal bağı kurar.

### 3. 📊 Büyük Veri Analitiği & Kümeleme (Unsupervised Learning)
* **Teknoloji:** `Scikit-Learn (K-Means Clustering)`
* **İşlev:** Veriler, herhangi bir etiketleme olmadan **Gözetimsiz Öğrenme** ile analiz edilir. Yapay zeka, benzer etkinlikleri kendi keşfettiği kümelerde (Clusters) toplar ve grafikte farklı renklerle (Örn: Spor, Sanat, Teknoloji) otomatik olarak gruplar.

### 4. 🐳 Mikroservis Mimarisi & Güvenlik
* **Altyapı:** Docker & Docker Compose
* **Sunucu:** Nginx (Reverse Proxy)
* **Güvenlik:** 12-Factor App prensiplerine uygun `.env` tabanlı konfigürasyon yönetimi.

---

## 🛠️ Teknoloji Yığını (Tech Stack)

| Alan | Teknoloji | Kullanım Amacı |
| :--- | :--- | :--- |
| **Backend** | Django (Python) | API ve İş Mantığı |
| **AI / ML** | PyTorch, Scikit-Learn | NLP ve Kümeleme Algoritmaları |
| **Graph** | NetworkX | Ağ Topolojisi Hesaplama |
| **Database** | PostgreSQL | İlişkisel Veri Saklama |
| **Frontend** | Bootstrap 5, Vis.js | UI ve Grafik Görselleştirme |
| **DevOps** | Docker, Nginx | Konteynerizasyon ve Sunucu |

---

## ⚡ Hızlı Kurulum (Quick Start)

Projeyi yerel ortamınızda ayağa kaldırmak için sadece **Docker** gereklidir.

### 1. Projeyi Klonlayın
```bash
git clone [https://github.com/yusufemre-kilic/ym341.git](https://github.com/yusufemre-kilic/ym341.git)
cd ym341