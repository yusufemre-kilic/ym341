from .models import Tag, Event
from sentence_transformers import SentenceTransformer, util
import networkx as nx
import faiss
import numpy as np
import logging
from sklearn.cluster import KMeans

# Loglama
logger = logging.getLogger(__name__)

# 1. MODELİ YÜKLE
print("⏳ AI Modeli Yükleniyor...")
try:
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("✅ AI Modeli Hazır!")
except Exception as e:
    logger.error(f"Model yüklenemedi: {e}")
    model = None

def build_faiss_index(embeddings):
    """
    FAISS Indeksi oluşturur. 
    Milyarlarca veri arasında O(log N) hızında arama yapmayı sağlar.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    return index

def analyze_and_tag_event(event_instance):
    """Etkinliği analiz eder ve etiketler."""
    if model is None: return ["HATA: Model Yok"]

    categories = [
        "Yazılım, Kodlama, Teknoloji, Bilgisayar ve AI",
        "Spor, Futbol, Basketbol, Antrenman, Sağlık, Kondisyon, Saha, Maç", 
        "Müzik, Konser, Enstrüman, Şarkı, Piyano, Keman",
        "Sanat, Resim, Tiyatro, Sergi, Heykel",
        "Bilim, Uzay, Fizik, Akademik, Yıldızlar, Gezegen",
        "Gezi, Doğa, Kamp, Seyahat, Yürüyüş"
    ]

    event_text = f"{event_instance.title}. {event_instance.description}"
    event_embedding = model.encode(event_text, convert_to_tensor=True)
    category_embeddings = model.encode(categories, convert_to_tensor=True)
    cosine_scores = util.cos_sim(event_embedding, category_embeddings)[0]

    found_tags = []
    for i, score in enumerate(cosine_scores):
        if score > 0.25:
            simple_tag_name = categories[i].split(",")[0].strip()
            tag_obj, _ = Tag.objects.get_or_create(name=simple_tag_name)
            event_instance.tags.add(tag_obj)
            found_tags.append(f"{simple_tag_name} (%{int(score*100)})")
    return found_tags

def semantic_search(query_text, top_k=5):
    """FAISS altyapısı ile anlamsal arama yapar."""
    if model is None: return []
    events = Event.objects.all()
    if not events.exists(): return []

    event_texts = [f"{e.title}. {e.description}" for e in events]
    event_embeddings = model.encode(event_texts)
    
    # --- FAISS GÜCÜ ---
    index = build_faiss_index(event_embeddings)
    query_embedding = model.encode([query_text]).astype('float32')
    
    # En yakın komşuları bul (D, mesafeler; I, indisler)
    D, I = index.search(query_embedding, top_k)

    results = []
    DISTANCE_THRESHOLD = 30.0
    for i, idx in enumerate(I[0]):
        if idx != -1: 
            distance = D[0][i]
            if distance < DISTANCE_THRESHOLD: # <--- İŞTE BU KONTROLÜ EKLEDİK
                event = events[int(idx)]
                results.append({
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "score": f"Dist: {distance:.2f}", 
                    "tags": [t.name for t in event.tags.all()]
                })
    
    return results

def generate_knowledge_graph():
    """
    K-Means ve NetworkX birleşimi. 
    Verileri otomatik kümeleyerek Bilgi Grafiği oluşturur.
    """
    if model is None: return {"nodes": [], "edges": []}

    events = Event.objects.all()
    if not events.exists(): return {"nodes": [], "edges": []}

    event_texts = [f"{e.title}. {e.description}" for e in events]
    embeddings = model.encode(event_texts)

    # 1. K-MEANS (Gözetimsiz Öğrenme)
    n_clusters = min(len(events), 5)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    # 2. Graph Kurulumu
    nodes_data = []
    colors = ["#ff0055", "#00d4ff", "#00ff9d", "#ffcc00", "#9d00ff"]

    for i, event in enumerate(events):
        cluster_id = int(labels[i])
        nodes_data.append({
            "id": event.id,
            "label": event.title,
            "group": cluster_id,
            "color": colors[cluster_id % len(colors)]
        })

    # 3. Benzerlik Bağları (Edges)
    cosine_scores = util.cos_sim(embeddings, embeddings)
    edge_list = []
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            score = float(cosine_scores[i][j])
            if score > 0.40:
                edge_list.append({
                    "from": events[i].id,
                    "to": events[j].id,
                    "value": score,
                    "title": f"Benzerlik: %{int(score*100)}"
                })

    print(f"🕸️ Graph Oluşturuldu: {len(nodes_data)} Düğüm, {len(edge_list)} Bağlantı")
    return {"nodes": nodes_data, "edges": edge_list}

def simulate_packet_routing(start_node_id, query_text, avoid_nodes=[]):
    """
    Leighton Ch 3.4.8: Fault Tolerance Routing
    avoid_nodes: Çökmüş/Ölü düğümlerin ID listesi. Paket buralara ASLA uğramaz.
    """
    if model is None: return {"path": [], "log": []}

    # 1. Hazırlık
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    current_node = Event.objects.filter(id=start_node_id).first()
    
    # Eğer başlangıç düğümü bile ölü ise simülasyonu başlatma
    if not current_node or current_node.id in avoid_nodes: 
        return {"error": "Başlangıç düğümü çökmüş durumda! (System Failure)"}

    path = [current_node.id]
    steps_log = []
    
    # Ziyaret edilenlere hem geçmişi hem de ölü düğümleri ekle ki geri dönmesin
    visited = {current_node.id}
    for dead_id in avoid_nodes:
        visited.add(dead_id)
    
    EDGE_THRESHOLD = 0.55 
    MAX_HOPS = 20 

    for step in range(MAX_HOPS):
        # Mevcut Konum
        current_text = f"{current_node.title} {current_node.description}"
        current_emb = model.encode(current_text, convert_to_tensor=True)
        current_dist_to_target = float(util.cos_sim(current_emb, query_embedding)[0][0])

        steps_log.append({
            "step": step + 1,
            "node": current_node.title,
            "score": f"{current_dist_to_target:.4f}"
        })

        # --- ADIM 1: Sağlam Komşuları Bul ---
        # Ölü olanları (avoid_nodes) ve daha önce geçtiklerimizi (visited) hariç tut
        all_events = Event.objects.exclude(id__in=visited)
        if not all_events.exists(): 
            steps_log.append({"info": "Gidecek hiçbir yer kalmadı."})
            break

        all_texts = [f"{e.title} {e.description}" for e in all_events]
        all_embs = model.encode(all_texts, convert_to_tensor=True)
        
        neighbor_scores = util.cos_sim(current_emb, all_embs)[0]
        
        valid_neighbors = []
        for i, score in enumerate(neighbor_scores):
            if score > EDGE_THRESHOLD:
                neighbor = all_events[i]
                # EKSTRA GÜVENLİK: Eğer ölü listesindeyse kesinlikle alma
                if neighbor.id not in avoid_nodes:
                    valid_neighbors.append(neighbor)

        if not valid_neighbors:
            steps_log.append({"info": "FAULT DETECTED: Tüm yollar tıkalı veya çökmüş."})
            break

        # --- ADIM 2: En İyisini Seç (Greedy) ---
        best_next_node = None
        best_next_score = -1

        for neighbor in valid_neighbors:
            n_text = f"{neighbor.title} {neighbor.description}"
            n_emb = model.encode(n_text, convert_to_tensor=True)
            n_score_to_target = float(util.cos_sim(n_emb, query_embedding)[0][0])
            
            if n_score_to_target > best_next_score:
                best_next_score = n_score_to_target
                best_next_node = neighbor

        # --- ADIM 3: İlerle ---
        if best_next_node:
            current_node = best_next_node
            visited.add(current_node.id)
            path.append(current_node.id)
        else:
            steps_log.append({"info": "Path blocked due to failures."})
            break

    return {"path": path, "log": steps_log}