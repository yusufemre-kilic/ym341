FROM python:3.13.1-slim

# Logları anlık görmek için
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Saat dilimi ayarı
RUN ln -sf /usr/share/zoneinfo/Europe/Istanbul /etc/localtime

# Gerekli kütüphaneler 
RUN apt-get update && apt-get install -y libpq-dev gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Gunicorn ile başlat (3 Worker = Aynı anda 3 işlem yapabilir)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "backend.wsgi:application"]