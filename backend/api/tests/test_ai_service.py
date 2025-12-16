# backend/api/tests/test_ai_service.py

from django.test import TestCase
from api.models import Event, Tag
from api.services import analyze_and_tag_event
from django.utils import timezone

class AIServiceTest(TestCase):
    def test_analyze_python_event(self):
        """İçinde 'Python' geçen bir etkinlik 'Yazılım' olarak etiketlenmeli"""
        
        # 1. Sanal bir etkinlik oluştur (Veritabanına kaydetmeden)
        event = Event.objects.create(
            title="Django Eğitimi",
            description="Python ile web geliştirme öğreniyoruz.",
            date=timezone.now()
        )

        # 2. Servisi çalıştır
        found_tags = analyze_and_tag_event(event)

        # 3. KONTROL ET (Assert)
        # 'Yazılım' etiketi bulundu mu?
        self.assertIn("Yazılım", found_tags)
        
        # Etkinliğe gerçekten eklendi mi?
        self.assertTrue(event.tags.filter(name="Yazılım").exists())

    def test_analyze_concert_event(self):
        """İçinde 'Konser' geçen bir etkinlik 'Müzik' olarak etiketlenmeli"""
        event = Event.objects.create(
            title="Bahar Şenliği",
            description="Büyük rock konseri sizi bekliyor!",
            date=timezone.now()
        )
        
        found_tags = analyze_and_tag_event(event)
        self.assertIn("Müzik", found_tags)