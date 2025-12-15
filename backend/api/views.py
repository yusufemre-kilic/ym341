from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from .models import Event
# Eğer Tag veya StudentProfile modelleri henüz yoksa hata vermesin diye try-except blokları içinde kullanacağız
try:
    from .models import Tag, StudentProfile
except ImportError:
    pass

# --- SAYFA YÖNLENDİRMELERİ ---

def login_page(request):
    return render(request, 'login.html')

def callback_page(request):
    return render(request, 'callback.html')

def ogrenci_page(request):
    return render(request, 'ogrenci-profil.html')

def ogretmen_page(request):
    return render(request, 'ogretmen-panel.html')

# --- API FONKSİYONLARI ---

@csrf_exempt
def verify_teacher_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip().lower()
            password = data.get('password', '')

            if email == settings.OGRETMEN_EMAIL and password == settings.OGRETMEN_SIFRESI:
                return JsonResponse({"status": "success"})
            elif email != settings.OGRETMEN_EMAIL:
                return JsonResponse({"error": "Bu e-posta yetkili değil!"}, status=401)
            else:
                return JsonResponse({"error": "Hatalı Şifre!"}, status=401)
        except Exception:
            return JsonResponse({"error": "Sunucu hatası"}, status=400)
    return JsonResponse({"error": "Sadece POST"}, status=405)

@csrf_exempt
def verify_student_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip().lower()
            password = data.get('password', '')

            if email != settings.OGRENCI_EMAIL:
                return JsonResponse({"error": "Öğrenci bulunamadı!"}, status=401)
            if password != settings.OGRENCI_SIFRESI:
                return JsonResponse({"error": "Hatalı Şifre!"}, status=401)

            return JsonResponse({"status": "success"})
        except Exception:
            return JsonResponse({"error": "Sunucu hatası"}, status=400)
    return JsonResponse({"error": "Sadece POST"}, status=405)

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
            return JsonResponse({"message": "Başarılı", "id": new_event.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Sadece POST"}, status=405)

# --- İŞTE EKSİK OLAN KISIM (BUNU EKLEMEZSEN SİSTEM ÇÖKER) ---
def recommend_events(request):
    # Şimdilik basitçe tüm etkinlikleri döndürelim (Hata vermemesi için)
    try:
        events = Event.objects.all().values('id', 'title', 'description', 'date')
        return JsonResponse({"recommendations": list(events)}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)