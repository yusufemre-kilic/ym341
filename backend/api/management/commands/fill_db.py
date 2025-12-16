# backend/api/management/commands/fill_db.py

from django.core.management.base import BaseCommand
from api.models import Event, Tag
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Veritabanını sahte verilerle doldurur'

    def handle(self, *args, **kwargs):
        self.stdout.write("Eski veriler temizleniyor...")
        Event.objects.all().delete()
        Tag.objects.all().delete()

        # Etiketler
        tags = {
            "Yazılım": Tag.objects.create(name="Yazılım"),
            "Müzik": Tag.objects.create(name="Müzik"),
            "Spor": Tag.objects.create(name="Spor"),
            "Sanat": Tag.objects.create(name="Sanat"),
            "Sinema": Tag.objects.create(name="Sinema"),
            "Bilim": Tag.objects.create(name="Bilim"),
        }

        # Veriler
        events_data = [
            ("Python Bootcamp", "Sıfırdan zirveye kodlama eğitimi.", "Yazılım"),
            ("Rock Festivali", "Kampüsün en gürültülü günü.", "Müzik"),
            ("Futbol Turnuvası", "Fakülteler arası dev maç.", "Spor"),
            ("Modern Sanat Sergisi", "Öğrenci çalışmaları sergisi.", "Sanat"),
            ("Yapay Zeka Konferansı", "Geleceğin teknolojileri konuşuluyor.", "Yazılım"),
        ]

        for title, desc, tag_key in events_data:
            e = Event.objects.create(
                title=title, 
                description=desc, 
                date=timezone.now() + datetime.timedelta(days=7)
            )
            e.tags.add(tags[tag_key])
            self.stdout.write(f"Eklendi: {title}")

        self.stdout.write(self.style.SUCCESS('Veritabanı başarıyla dolduruldu! 🚀'))