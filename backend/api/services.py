# backend/api/services.py

from .models import Tag
from sentence_transformers import SentenceTransformer, util
import logging

# Loglama (Hata ayıklamak için profesyonel yaklaşım)
logger = logging.getLogger(__name__)

# 1. MODELİ YÜKLE
# Bu işlem uygulama ilk açıldığında 1 kere yapılır.
# 'paraphrase-multilingual-MiniLM-L12-v2' modeli Türkçe dahil 50+ dili destekler.
print("⏳ AI Modeli Yükleniyor... (İlk seferde biraz sürebilir)")
try:
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("✅ AI Modeli Hazır!")
except Exception as e:
    logger.error(f"Model yüklenemedi: {e}")
    model = None

def analyze_and_tag_event(event_instance):
    """
    Etkinlik metnini vektöre çevirir ve tanımlı kategorilerle
    anlamsal benzerliğini (Cosine Similarity) ölçer.
    """
    if model is None:
        return ["HATA: AI Modeli Yüklenemedi"]

# 2. HEDEF KATEGORİLER (Güncellendi)
    # Kategorileri ne kadar detaylı tanımlarsak AI o kadar iyi anlar.
    categories = [
        "Yazılım, Kodlama, Teknoloji ve Bilgisayar",
        "Spor, Futbol, Basketbol, Antrenman ve Sağlık", # Detay ekledik
        "Müzik, Konser, Enstrüman ve Şarkı",
        "Sanat, Resim, Tiyatro ve Sergi",
        "Bilim, Uzay, Fizik ve Akademik",
        "Sinema, Film, Yönetmen ve Oyuncu",
        "Gezi, Doğa, Kamp ve Seyahat",
        "Kariyer, İş Dünyası, Girişimcilik ve Staj"
    ]

    # Etkinlik metnini birleştir
    event_text = f"{event_instance.title}. {event_instance.description}"

    # 3. VEKTÖR HESAPLAMA (Embedding)
    # Etkinliğin ve kategorilerin uzaydaki yerini buluyoruz
    event_embedding = model.encode(event_text, convert_to_tensor=True)
    category_embeddings = model.encode(categories, convert_to_tensor=True)

    # 4. BENZERLİK ÖLÇÜMÜ (Cosine Similarity)
    # Hangi kategoriyle ne kadar uyuşuyor?
    cosine_scores = util.cos_sim(event_embedding, category_embeddings)[0]

    found_tags = []
    
    # Benzerlik Eşiği (0.0 ile 1.0 arası)
    # 0.25 üzerindeki eşleşmeleri kabul et diyoruz.
    THRESHOLD = 0.25 

    for i, score in enumerate(cosine_scores):
        if score > THRESHOLD:
            category_name = categories[i]
            
            # Kategori ismini sadeleştir (Örn: "Yazılım ve Teknoloji" -> "Yazılım")
            # Tag olarak kısa halini kaydedelim
            simple_tag_name = category_name.split(" ")[0] 
            
            tag_obj, _ = Tag.objects.get_or_create(name=simple_tag_name)
            event_instance.tags.add(tag_obj)
            found_tags.append(f"{simple_tag_name} (%{score:.2f})")

    return found_tags