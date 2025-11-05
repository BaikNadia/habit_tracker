FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем директории для статики и медиа (если нужны)
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles
RUN mkdir -p /app/mediafiles && chmod -R 755 /app/mediafiles

# Собираем статику (не обязательно здесь, но можно)
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Запуск Gunicorn (в production)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
# FROM python:3.11
#
# WORKDIR /app
#
# # Установка системных зависимостей
# RUN apt-get update \
#     && apt-get install -y gcc libpq-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
#
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install gunicorn
#
# COPY . .
#
# # Создаём и даём права на директорию для статистических файлов
# RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles
#
# EXPOSE 8000
#
# CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]