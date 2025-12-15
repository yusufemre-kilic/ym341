from django.contrib import admin
from .models import Event

# Event tablosunu admin panelinde görünür yap
admin.site.register(Event)