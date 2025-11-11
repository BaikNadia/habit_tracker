FROM python:3.11-slim

WORKDIR /app

<<<<<<< HEAD
# Установка зависимостей
=======
# Установка системных зависимостей
>>>>>>> server-changes
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

<<<<<<< HEAD
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["celery", "-A", "your_project", "worker", "--loglevel=info"]
=======
# Копирование requirements и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

CMD ["celery", "-A", "config", "worker", "--loglevel=info"]
>>>>>>> server-changes
