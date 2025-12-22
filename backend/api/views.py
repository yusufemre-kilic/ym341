from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os  # <--- YENİ: İşletim sistemi değişkenlerini (.env) okumak için
from .models import Event, Tag 
from .services import analyze_and_tag_event, semantic_search, generate_knowledge_graph
from .services import simulate_packet_routing
from django.utils import timezone
import datetime

# --- SAYFA YÖNLENDİRMELERİ ---

def login_page(request):
    return render(request, 'login.html')

def callback_page(request):
    return redirect('ogrenci')

def ogrenci_page(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'ogrenci-profil.html', {'events': events})

def ogretmen_page(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'ogretmen-panel.html', {'events': events})

# --- API FONKSİYONLARI (GÜVENLİK GÜNCELLEMESİ) ---

@csrf_exempt
def verify_student_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # .env dosyasından gerçek değerleri okuyoruz
            env_email = os.environ.get('OGRENCI_EMAIL')   # yusuf@dogus.edu.tr
            env_pass = os.environ.get('OGRENCI_SIFRESI')  # 5678

            # Eşleşme kontrolü
            if email == env_email and password == env_pass:
                return JsonResponse({'status': 'ok'})
            
            return JsonResponse({'status': 'error', 'message': 'Hatalı bilgiler!'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'detail': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
def verify_teacher_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # .env dosyasından gerçek değerleri okuyoruz
            env_email = os.environ.get('OGRETMEN_EMAIL')  # yasemin@dogus.edu.tr
            env_pass = os.environ.get('OGRETMEN_SIFRESI') # 1234

            if email == env_email and password == env_pass:
                return JsonResponse({'status': 'ok'})
            
            return JsonResponse({'status': 'error', 'message': 'Hatalı bilgiler!'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'detail': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

# --- DİĞER FONKSİYONLAR (AYNI KALDI) ---

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            date = timezone.now() + datetime.timedelta(days=7)

            new_event = Event.objects.create(
                title=title,
                description=description,
                date=date
            )
            
            # AI Analizi
            tags_found = analyze_and_tag_event(new_event)

            return JsonResponse({
                "message": "Etkinlik kaydedildi ve AI analiz etti!",
                "ai_tags": tags_found
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Sadece POST"}, status=400)

@csrf_exempt
def search_events_api(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if not query: return JsonResponse({"results": []})
        try:
            results = semantic_search(query)
            return JsonResponse({"results": results})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def graph_data_api(request):
    """Network Grafiği verisini JSON olarak döner"""
    try:
        graph_data = generate_knowledge_graph()
        return JsonResponse(graph_data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def graph_page_view(request):
    """Grafik görselleştirme sayfasını açar"""
    return render(request, 'graph.html')

@csrf_exempt
def routing_api(request):
    """Routing Simülasyonu (Fault Tolerance Destekli)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            start_node = data.get('start_node_id')
            query = data.get('query')
            
            # Frontend'den gelen ölü düğüm listesi (yoksa boş liste)
            dead_nodes = data.get('dead_nodes', []) 
            
            result = simulate_packet_routing(start_node, query, avoid_nodes=dead_nodes)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "POST required"}, status=400)
    
# Yer tutucular
@csrf_exempt
def recommend_events(request): return JsonResponse({"status": "ok"})
@csrf_exempt
def save_interests(request): return JsonResponse({"status": "ok"})
@csrf_exempt
def reset_interests(request): return JsonResponse({"status": "ok"})