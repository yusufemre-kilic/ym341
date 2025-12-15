from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q 
import json
from .models import Event, Tag, StudentProfile

# ==========================================
# 1. EKSİK OLAN SAYFA YÖNLENDİRMELERİ (BURASI ÇOK ÖNEMLİ)
# ==========================================
def login_page(request):
    return render(request, 'login.html')

def callback_page(request):
    return render(request, 'callback.html')

def ogrenci_page(request):
    return render(request, 'ogrenci-profil.html')

def ogretmen_page(request):
    return render(request, 'ogretmen-panel.html')

# ==========================================
# 2. YAPAY ZEKA (OTOMATİK ETİKETLEME)
# ==========================================
def analyze_and_tag(event_instance):
    keywords = {
        "Yazılım": ["python", "java", "kodlama", "yazılım", "bilgisayar", "ai", "yapay zeka", "web", "react", "django"],
        "Spor": ["futbol", "basketbol", "voleybol", "koşu", "turnuva", "maç", "spor", "fitness", "yüzme"],
        "Müzik": ["konser", "gitar", "piyano", "şarkı", "dinleti", "müzik", "orkestra", "sahne"],
        "Sanat": ["resim", "tiyatro", "sinema", "sergi", "sanat", "boyama", "heykel", "fotoğraf"],
        "Bilim": ["fizik", "kimya", "biyoloji", "deney", "bilim", "uzay", "robot"],
        "Sinema": ["film", "sinema", "gösterim", "izle", "yönetmen", "oyuncu"]
    }
    full_text = (event_instance.title + " " + event_instance.description).lower()
    found_tags = []
    for category, words in keywords.items():
        if any(word in full_text for word in words):
            tag_obj, _ = Tag.objects.get_or_create(name=category)
            event_instance.tags.add(tag_obj)
            found_tags.append(category)
    return found_tags

# ==========================================
# 3. API FONKSİYONLARI
# ==========================================

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_event = Event.objects.create(
                title=data['title'],
                description=data['description'],
                date=data.get('date')
            )
            added_tags = analyze_and_tag(new_event)
            return JsonResponse({"message": f"Kayıt Başarılı. Eklenen Etiketler: {added_tags}", "id": new_event.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def recommend_events(request):
    try:
        student, _ = StudentProfile.objects.get_or_create(email=settings.OGRENCI_EMAIL)
        my_interests = student.interests.all()
        has_interests = my_interests.exists()
        events = []
        message = ""

        if not has_interests:
            events = Event.objects.all().order_by('-date')[:5]
            message = "Henüz ilgi alanı seçmediniz, işte son etkinlikler:"
        else:
            query = Q(tags__in=my_interests)
            for interest in my_interests:
                query |= Q(description__icontains=interest.name) | Q(title__icontains=interest.name)
            
            events = Event.objects.filter(query).distinct().order_by('-date')
            
            if not events:
                events = Event.objects.all().order_by('-created_at')[:3]
                tags_str = ", ".join([t.name for t in my_interests])
                message = f"'{tags_str}' alanında etkinlik yok ama şunlar popüler:"
            else:
                message = "Sizin için seçtiklerimiz:"

        data = []
        for e in events:
            tags = [t.name for t in e.tags.all()]
            data.append({
                "title": e.title,
                "description": e.description,
                "date": e.date,
                "tags": tags
            })

        return JsonResponse({"message": message, "recommendations": data, "has_interests": has_interests})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def save_interests(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_tags = data.get('tags', [])
            student, _ = StudentProfile.objects.get_or_create(email=settings.OGRENCI_EMAIL)
            student.interests.clear()
            for tag_name in selected_tags:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                student.interests.add(tag_obj)
            return JsonResponse({"message": "Kaydedildi!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def reset_interests(request):
    if request.method == 'POST':
        try:
            student, _ = StudentProfile.objects.get_or_create(email=settings.OGRENCI_EMAIL)
            student.interests.clear()
            return JsonResponse({"message": "Sıfırlandı!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def verify_teacher_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('email') == settings.OGRETMEN_EMAIL and data.get('password') == settings.OGRETMEN_SIFRESI:
            return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Hatalı Giriş"}, status=401)

@csrf_exempt
def verify_student_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('email') == settings.OGRENCI_EMAIL and data.get('password') == settings.OGRENCI_SIFRESI:
            StudentProfile.objects.get_or_create(email=settings.OGRENCI_EMAIL)
            return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Hatalı Giriş"}, status=401)