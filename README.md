# 🧠 Kampüs AI - Akıllı Etkinlik & Bilgi Grafiği Sistemi (YM341)

**Yapay Zeka Destekli, Graph-Tabanlı ve Büyük Veri Uyumlu Etkinlik Yönetim Platformu**

Bu proje, geleneksel veritabanı sorgularının ötesine geçerek; **NLP (Doğal Dil İşleme)**, **Graph Theory (Çizge Teorisi)** ve **Vektör İndeksleme** teknolojilerini kullanarak etkinlikler arasındaki anlamsal ilişkileri analiz eden yeni nesil bir yönetim sistemidir.

![Graph View](backend/static/images/graph.png) ---

## 🚀 Projenin Teknik Derinliği (Key Engineering Features)

Bu sistem sadece CRUD işlemleri yapan bir web sitesi değildir. Arka planda çalışan ileri seviye mühendislik çözümleri şunlardır:

### 1. 🕸️ Dinamik Bilgi Grafiği & Fizik Motoru
* **Teknoloji:** NetworkX, Vis.js (BarnesHut Algoritması)
* **Mantık:** Sistemdeki her etkinlik bir "Düğüm" (Node) olarak kabul edilir. İçerik benzerlikleri hesaplanarak düğümler arası "Kenarlar" (Edges) matematiksel olarak oluşturulur.
* **Optimizasyon:** Büyük veri setlerinde tarayıcıyı kilitlememek için **Barnes-Hut** algoritması kullanılarak $O(N \log N)$ karmaşıklığında fizik hesaplaması yapılır. "Big Bang" efekti ile düğümler ekrana homojen olarak dağıtılır.

### 2. ⚡ FAISS Destekli Semantik Arama (Big Data Search)
* **Teknoloji:** Sentence-Transformers (BERT), Facebook AI Similarity Search (FAISS)
* **Farkı:** Klasik `LIKE %query%` sorguları yerine, veriler 384 boyutlu vektör uzayına (Embeddings) taşınır.
* **Performans:** Milyonlarca veri arasında en yakın komşuyu bulmak için **FAISS İndeksleme** kullanılır. Bu sayede arama hızı milisaniyeler seviyesindedir.
* **Örnek:** "Keman" aratıldığında, içinde kelime geçmese bile "Beethoven Gecesi"ni bulur.

### 3. 📊 Gözetimsiz Öğrenme & Kümeleme (Clustering)
* **Teknoloji:** Scikit-Learn (K-Means Clustering)
* **İşlev:** Veriler, herhangi bir etiketleme olmadan **Gözetimsiz Öğrenme** ile analiz edilir. Yapay zeka, benzer etkinlikleri kendi keşfettiği kümelerde (Clusters) toplar ve grafikte farklı renklerle (Örn: Spor, Sanat, Teknoloji) otomatik olarak gruplar.

### 4. 🐳 Mikroservis Mimarisi
* **Altyapı:** Docker & Docker Compose
* **Sunucu:** Nginx (Reverse Proxy)
* **Güvenlik:** 12-Factor App prensiplerine uygun `.env` tabanlı konfigürasyon yönetimi.

---

## 🛠️ Teknoloji Yığını (Tech Stack)

| Alan | Teknoloji | Kullanım Amacı |
|---|---|---|
| **Backend** | Django (Python 3.13) | RESTful API ve İş Mantığı |
| **AI / NLP** | PyTorch, BERT | Metinleri Vektöre Çevirme (Embeddings) |
| **Big Data** | **FAISS (Facebook AI)** | Yüksek Performanslı Vektör Arama |
| **Graph** | NetworkX, Vis.js | Ağ Topolojisi ve Görselleştirme |
| **ML** | Scikit-Learn (K-Means) | Otomatik Veri Kümeleme |
| **Database** | PostgreSQL | İlişkisel Veri Saklama |
| **DevOps** | Docker, Nginx | Konteynerizasyon ve Sunucu |

---

## ⚡ Hızlı Kurulum (Quick Start)

Projeyi yerel ortamınızda ayağa kaldırmak için sadece **Docker** gereklidir.

### 1. Projeyi Klonlayın
```bash
git clone [https://github.com/yusufemre-kilic/ym341.git](https://github.com/yusufemre-kilic/ym341.git)
cd ym341