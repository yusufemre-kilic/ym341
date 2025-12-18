from django.core.management.base import BaseCommand
from api.models import Event, Tag
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Veritabanını sahte verilerle doldurur'

    def handle(self, *args, **kwargs):
        self.stdout.write("Eski veriler temizleniyor...")
        # Önce eski kayıtları silelim
        Event.objects.all().delete()
        Tag.objects.all().delete()

        # NLP Test Verileri 
        # Format: (Başlık, Açıklama, Eski Manuel Etiket -Artık kullanılmıyor-)
        events_data = [
            ("Python Bootcamp", "Sıfırdan zirveye kodlama eğitimi.", "Yazılım"), 
            ("Yeşil Sahaların Yıldızları", "Kondisyonuna güvenenler sahaya!", "Spor"),
            ("Beethoven Gecesi", "Keman ve piyano resitali.", "Müzik"),
            ("Tuvaldeki Renkler", "Yağlı boya çalışmalarımızı sergiliyoruz.", "Sanat"),
            ("Gökyüzü Gözlemi", "Teleskoplarla yıldızlara bakıyoruz.", "Bilim"),
            ("Start-Up Zirvesi", "Girişimcilik ekosistemi ve yatırımcılar.", "Yazılım"),
        ]

        # Döngü ile verileri ekle ve AI servisini çağır
        for title, desc, _ in events_data:
            # 1. Etkinliği Oluştur
            e = Event.objects.create(
                title=title, 
                description=desc, 
                date=timezone.now() + datetime.timedelta(days=7)
            )
            
            # 2. AI Servisini Çağır ve Etiketle
            try:
                from api.services import analyze_and_tag_event
                found_tags = analyze_and_tag_event(e)
                self.stdout.write(f"✅ Eklendi: {title} -> AI Buldu: {found_tags}")
            except Exception as error:
                self.stdout.write(self.style.ERROR(f"❌ AI Hatası ({title}): {error}"))

        self.stdout.write(self.style.SUCCESS('Veritabanı başarıyla dolduruldu! 🚀'))