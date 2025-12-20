from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api import views
from api import views

# Artık views.py içinde bu fonksiyonların hepsi VAR. Hata vermeyecek.
from api.views import (
    login_page, callback_page, ogrenci_page, ogretmen_page, 
    create_event, verify_teacher_password, verify_student_password, 
    recommend_events, save_interests, reset_interests
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='login'),
    path('callback/', callback_page, name='callback'),
    path('ogrenci/', ogrenci_page, name='ogrenci'),
    path('ogretmen/', ogretmen_page, name='ogretmen'),
    path('api/events/create/', create_event, name='create_event'),
    path('api/verify-teacher/', verify_teacher_password, name='verify_teacher'),
    path('api/verify-student/', verify_student_password, name='verify_student'),
    path('api/events/recommend/', recommend_events, name='recommend_events'),
    path('api/student/interests/', save_interests, name='save_interests'),
    path('api/student/reset/', reset_interests, name='reset_interests'),
    path('api/search/', views.search_events_api, name='search_api'),
    path('api/create-event/', views.create_event, name='create_event'),
    path('api/graph-data/', views.graph_data_api, name='graph_api'),
    path('graph/', views.graph_page_view, name='graph_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])