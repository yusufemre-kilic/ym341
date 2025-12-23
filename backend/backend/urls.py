from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api import views

urlpatterns = [
    # --- YÖNETİM ---
    path('admin/', admin.site.urls),

    # --- HTML SAYFALARI (FRONTEND) ---
    path('', views.login_page, name='login'),
    path('callback/', views.callback_page, name='callback'),
    path('ogrenci/', views.ogrenci_page, name='ogrenci'),
    path('ogretmen/', views.ogretmen_page, name='ogretmen'),
    path('graph/', views.graph_page_view, name='graph_page'),

    # --- API ENDPOINTLERİ (BACKEND) ---
    # Giriş Doğrulama
    path('api/verify-teacher/', views.verify_teacher_password, name='verify_teacher'),
    path('api/verify-student/', views.verify_student_password, name='verify_student'),
    
    # Etkinlik İşlemleri
    path('api/create-event/', views.create_event, name='create_event'),
    path('api/search-events/', views.search_events_api, name='search_events_api'),
    path('api/events/recommend/', views.recommend_events, name='recommend_events'),
    
    # Öğrenci İlgi Alanları
    path('api/student/interests/', views.save_interests, name='save_interests'),
    path('api/student/reset/', views.reset_interests, name='reset_interests'),

    # Grafik ve Routing (Network)
    path('api/graph-data/', views.graph_data_api, name='graph_api'),
    path('api/routing/', views.routing_api, name='routing_api'),
]

# --- STATİK DOSYA VE RESİMLERİN GÖSTERİLMESİ ---
if settings.DEBUG:
    # 1. Medya dosyaları (varsa)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # 2. Statik dosyalar (CSS, JS, Images - Logolar için burası kritik)
    # Eğer settings.py içinde STATICFILES_DIRS tanımlıysa ilk klasörü kullanır
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        # Tanımlı değilse standart STATIC_ROOT'a bakar
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)