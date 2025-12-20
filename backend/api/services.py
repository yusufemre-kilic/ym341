from .models import Tag, Event  # <--- DÜZELTME: Event EKLENDİ!
from sentence_transformers import SentenceTransformer, util
import networkx as nx
import logging

# Loglama
logger = logging.getLogger(__name__)

# 1. MODELİ YÜKLE
print("⏳ AI Modeli Yükleniyor... (Bu işlem bir kez yapılır)")
try:
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("✅ AI Modeli Hazır!")
except Exception as e:
    logger.error(f"Model yüklenemedi: {e}")
    model = None

def analyze_and_tag_event(event_instance):
    """
    Etkinlik metnini vektöre çevirir ve tanımlı kategorilerle
    anlamsal benzerliğini ölçer.
    """
    if model is None:
        return ["HATA: AI Modeli Yüklenemedi"]

    # KATEGORİLER
    categories = [
        "Yazılım, Kodlama, Teknoloji, Bilgisayar ve AI",
        "Spor, Futbol, Basketbol, Antrenman, Sağlık, Kondisyon, Saha, Yeşil Saha, Maç", 
        "Müzik, Konser, Enstrüman, Şarkı, Piyano, Keman",
        "Sanat, Resim, Tiyatro, Sergi, Heykel",
        "Bilim, Uzay, Fizik, Akademik, Yıldızlar, Gezegen",
        "Sinema, Film, Yönetmen, Oyuncu",
        "Gezi, Doğa, Kamp, Seyahat, Yürüyüş",
        "Kariyer, İş Dünyası, Girişimcilik, Staj"
    ]

    event_text = f"{event_instance.title}. {event_instance.description}"
    
    # Vektör Hesaplama
    event_embedding = model.encode(event_text, convert_to_tensor=True)
    category_embeddings = model.encode(categories, convert_to_tensor=True)
    cosine_scores = util.cos_sim(event_embedding, category_embeddings)[0]

    found_tags = []
    THRESHOLD = 0.25 

    for i, score in enumerate(cosine_scores):
        if score > THRESHOLD:
            category_name = categories[i]
            simple_tag_name = category_name.split(",")[0].strip() # İlk kelimeyi al
            
            tag_obj, _ = Tag.objects.get_or_create(name=simple_tag_name)
            event_instance.tags.add(tag_obj)
            found_tags.append(f"{simple_tag_name} (%{score:.2f})")

    return found_tags

def semantic_search(query_text, top_k=3):
    """
    Kullanıcının yazdığı metni (query) alır, veritabanındaki 
    TÜM etkinliklerle anlamsal olarak karşılaştırır.
    """
    if model is None:
        return []

    # 1. Tüm etkinlikleri çek
    events = Event.objects.all()
    if not events.exists():
        return []

    # 2. Etkinlik metinlerini hazırla
    event_texts = [f"{e.title}. {e.description}" for e in events]
    
    # 3. Vektör Hesaplamaları (Query vs Events)
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    event_embeddings = model.encode(event_texts, convert_to_tensor=True)

    # 4. Benzerlikleri hesapla
    hits = util.semantic_search(query_embedding, event_embeddings, top_k=top_k)[0]

    # 5. Sonuçları hazırla
    results = []
    for hit in hits:
        score = hit['score']
        if score > 0.25: # %25'ten düşük benzerlikleri getirme
            idx = hit['corpus_id']
            event = events[int(idx)]
            results.append({
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "score": f"%{int(score * 100)}",
                "tags": [t.name for t in event.tags.all()]
            })
            
    return results

def generate_knowledge_graph():
    """
    Tüm etkinlikleri analiz eder ve bir Bilgi Grafiği oluşturur.
    Benzerlik skoru 0.20'nin üzerinde olanları birbirine bağlar.
    """
    if model is None:
        return {"nodes": [], "edges": []}

    events = Event.objects.all()
    if not events.exists():
        return {"nodes": [], "edges": []}

    # 1. Metinleri Vektöre Çevir
    event_texts = [f"{e.title}. {e.description}" for e in events]
    embeddings = model.encode(event_texts, convert_to_tensor=True)
    
    # 2. Benzerlik Matrisini Çıkar
    cosine_scores = util.cos_sim(embeddings, embeddings)

    # 3. Graph Oluştur (NetworkX)
    G = nx.Graph()
    
    nodes_data = []
    for event in events:
        # Her bir düğüm (Node) bir etkinliktir
        nodes_data.append({"id": event.id, "label": event.title, "group": "Event"})
        G.add_node(event.id)

    # 4. Kenarları (Edges) Hesapla
    edge_list = []
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            score = float(cosine_scores[i][j])
            
            # EŞİK DEĞERİ: %20'den fazla benzeyenleri bağla
            if score > 0.20: 
                edge_list.append({
                    "from": events[i].id,
                    "to": events[j].id,
                    "value": score,
                    "title": f"Benzerlik: %{int(score*100)}"
                })

    print(f"🕸️ Graph Oluşturuldu: {len(nodes_data)} Düğüm, {len(edge_list)} Bağlantı")
    return {"nodes": nodes_data, "edges": edge_list}