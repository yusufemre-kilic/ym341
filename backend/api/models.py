from django.db import models

# 1. ETİKETLER (İlgi Alanları)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True) # Örn: Yazılım, Müzik, Spor
    
    def __str__(self):
        return self.name

# 2. ÖĞRENCİ PROFİLİ
class StudentProfile(models.Model):
    # E-posta adresini kimlik olarak kullanıyoruz
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, default="Öğrenci")
    # Öğrencinin seçtiği ilgi alanları (Çoka-çok ilişki)
    interests = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.email

# 3. ETKİNLİK
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    time = models.TimeField(null=True, blank=True) 
    location = models.CharField(max_length=255, default="Kampüs")
    organizer = models.CharField(max_length=100, default="Rektörlük")
    created_at = models.DateTimeField(auto_now_add=True)
    # Etkinliğin etiketleri (Örn: Bu bir "Müzik" etkinliğidir)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title