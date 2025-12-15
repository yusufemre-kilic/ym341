from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Artık views dosyasında hepsi var, hata vermez:
from api.views import (
    login_page, callback_page, ogrenci_page, ogretmen_page, 
    create_event, verify_teacher_password, verify_student_password, 
    recommend_events
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='login'),
    path('callback/', callback_page, name='callback'),
    path('ogrenci/', ogrenci_page, name='ogrenci'),
    path('ogretmen/', ogretmen_page, name='ogretmen'),
    
    # API Yolları
    path('api/events/create/', create_event, name='create_event'),
    path('api/verify-teacher/', verify_teacher_password, name='verify_teacher'),
    path('api/verify-student/', verify_student_password, name='verify_student'),
    path('api/events/recommend/', recommend_events, name='recommend_events'),
]

# Resim ayarı (En kritik yer burası)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])