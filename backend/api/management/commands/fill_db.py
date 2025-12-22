from django.core.management.base import BaseCommand
from api.models import Event, Tag
from django.utils import timezone
import datetime
import random
from api.services import model


class Command(BaseCommand):
    help = 'Veritabanını otomatik olarak rastgele ama mantıklı verilerle doldurur.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('⏳ Yapay Zeka rastgele senaryolar üretiyor...'))

        # Rastgele Veri Havuzu
        topics = [
            ("Yapay Zeka", "Teknoloji"), ("Python", "Teknoloji"), ("Docker", "Teknoloji"),
            ("Futbol", "Spor"), ("Basketbol", "Spor"), ("Yoga", "Spor"),
            ("Keman", "Sanat"), ("Modern Sanat", "Sanat"), ("Tiyatro", "Sanat"),
            ("Uzay Fiziği", "Bilim"), ("Kuantum", "Bilim"), ("Genetik", "Bilim")
        ]
        
        actions = ["Atölyesi", "Konferansı", "Zirvesi", "Eğitimi", "Turnuvası", "Gösterisi", "Buluşması"]
        
        adjectives = ["İleri Seviye", "Başlangıç İçin", "Uluslararası", "Geleneksel", "Yenilikçi", "Kampüs İçi"]

        # Kaç tane veri üretelim? (Şimdilik 100 yapalım, istersen 1000 yap)
        TOTAL_EVENTS = 10

        for i in range(TOTAL_EVENTS):
            topic, category = random.choice(topics)
            action = random.choice(actions)
            adj = random.choice(adjectives)

            title = f"{adj} {topic} {action}"
            description = f"Bu etkinlikte {topic} alanında uzmanlarla bir araya geliyoruz. {category} tutkunları için harika bir fırsat."

            # Etkinliği oluştur
            event = Event.objects.create(
                title=title,
                description=description,
                date="2025-12-20",
                time="14:00",
                location="Kampüs Merkezi",
                organizer="Yapay Zeka Botu"
            )

            # AI Tagleme (analyze_and_tag_event fonksiyonunu manuel simüle ediyoruz hız için)
            tag, _ = Tag.objects.get_or_create(name=category)
            event.tags.add(tag)

            # İlerleme çubuğu gibi çıktı ver
            if i % 10 == 0:
                self.stdout.write(f"✅ {i} etkinlik üretildi...")

        self.stdout.write(self.style.SUCCESS(f'🚀 BAŞARILI! Toplam {TOTAL_EVENTS} adet yeni etkinlik veritabanına eklendi.'))