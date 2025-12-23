import os
from pathlib import Path

# Proje ana dizini (manage.py'nin olduğu yer)
BASE_DIR = Path(__file__).resolve().parent.parent

# GÜVENLİK AYARLARI
SECRET_KEY = 'django-insecure-test-key'
DEBUG = True
ALLOWED_HOSTS = ['*'] # Her yerden erişime izin ver

# UYGULAMALAR
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api', # Senin uygulaman
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # HTML dosyaların burada
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# VERİTABANI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ŞİFRE DOĞRULAMA (Basitlik için boş bırakılabilir ama standart kalsın)
AUTH_PASSWORD_VALIDATORS = []

# DİL VE SAAT
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# --- STATİK DOSYALAR (LOGOLAR İÇİN KRİTİK AYAR) ---
STATIC_URL = '/static/'

# Senin resimlerin 'backend/static' içinde olduğu için:
STATICFILES_DIRS = [
    BASE_DIR / 'backend' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ÖZEL DEĞİŞKENLER
OGRETMEN_SIFRESI = "1234"
OGRETMEN_EMAIL = "yasemin@dogus.edu.tr"
OGRENCI_EMAIL = "yusuf@dogus.edu.tr"
OGRENCI_SIFRESI = "5678"