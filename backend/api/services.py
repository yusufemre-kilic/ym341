# backend/api/services.py

from .models import Tag

def analyze_and_tag_event(event_instance):
    """
    Bir etkinlik nesnesini alır, başlık ve açıklamasını analiz eder,
    ilgili etiketleri bulup veritabanına kaydeder ve etkinliğe ekler.
    Geriye eklenen etiketlerin listesini döndürür.
    """
    keywords = {
        "Yazılım": ["python", "java", "kodlama", "yazılım", "bilgisayar", "ai", "yapay zeka", "web", "react", "django"],
        "Spor": ["futbol", "basketbol", "voleybol", "koşu", "turnuva", "maç", "spor", "fitness", "yüzme"],
        "Müzik": ["konser", "gitar", "piyano", "şarkı", "dinleti", "müzik", "orkestra", "sahne", "rock", "pop"],
        "Sanat": ["resim", "tiyatro", "sinema", "sergi", "sanat", "boyama", "heykel", "fotoğraf"],
        "Bilim": ["fizik", "kimya", "biyoloji", "deney", "bilim", "uzay", "robot"],
        "Sinema": ["film", "sinema", "gösterim", "izle", "yönetmen", "oyuncu"]
    }

    # Metinleri birleştir ve küçült
    full_text = (event_instance.title + " " + event_instance.description).lower()

    found_tags = []
    for category, words in keywords.items():
        # Eğer kelimelerden biri metinde geçiyorsa
        if any(word in full_text for word in words):
            tag_obj, _ = Tag.objects.get_or_create(name=category)
            event_instance.tags.add(tag_obj)
            found_tags.append(category)
    
    return found_tags