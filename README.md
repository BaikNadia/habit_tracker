# 🧘‍♀️ Habit Tracker — Трекер полезных привычек

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST](https://img.shields.io/badge/Django%20REST%20Framework-3.14%2B-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-5.3%2B-green?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-7.2%2B-red?logo=redis&logoColor=white)](https://redis.io/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub Stars](https://img.shields.io/github/stars/BaikNadia/habit-tracker?style=social)](https://github.com/BaikNadia/habit-tracker)

**REST API на Django для создания, отслеживания и получения напоминаний о полезных привычках через Telegram**  
Полноценная система для формирования полезных привычек с автоматическими напоминаниями и аналитикой прогресса.

---

**👩‍💻 Автор:** [BaikNadia](https://github.com/BaikNadia)  
**📦 Репозиторий:** [Habit Tracker](https://github.com/BaikNadia/habit-tracker)  
**📜 Лицензия:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)

---

## 📌 Основные возможности
📝 Создание, редактирование и удаление привычек  
🔒 Личный кабинет: пользователи видят только свои привычки  
🌍 Публичные привычки: просмотр чужих публичных привычек  
⏰ Пагинация (5 привычек на страницу)  
📱 Интеграция с Telegram: автоматические напоминания  
✅ Валидация по бизнес-правилам  
🔐 Аутентификация через JWT  
📚 Документация API через Swagger  

### Бизнес-правила валидации:
- Время выполнения ≤ 120 секунд
- Нельзя указывать и вознаграждение, и связанную привычку одновременно
- Связанная привычка должна быть «приятной»
- Периодичность — от 1 до 7 дней

## 🛠 Технологии
**Backend**: Python 3.11, Django 4.2, Django REST Framework  
**Аутентификация**: djangorestframework-simplejwt  
**Асинхронные задачи**: Celery + Redis  
**База данных**: PostgreSQL (продакшн), SQLite (тесты)  
**Интеграция**: Telegram Bot API  
**Документация**: drf-yasg (Swagger)  
**Тестирование**: pytest, coverage, flake8  
**Контейнеризация**: Docker, Docker Compose  
**CI/CD**: GitHub Actions  

## 🚀 Быстрый запуск с Docker Compose
1. Клонирование репозитория:  
`git clone https://github.com/BaikNadia/habit_tracker.git`  
`cd habit_tracker`

2. Настройка переменных окружения - создайте файл `.env` в корне проекта:
SECRET_KEY=ваш-секретный-ключ-для-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DB_ENGINE=django.db.backends.postgresql
DB_NAME=habit_tracker
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
TELEGRAM_BOT_TOKEN=ваш-токен-бота-телеграм


3. Запуск проекта:  
`docker compose up --build`  
Приложение будет доступно по адресу: http://localhost:8000

## 🛠 Локальная разработка (без Docker)
1. Клонирование и настройка окружения:  
`git clone https://github.com/BaikNadia/habit_tracker.git`  
`cd habit_tracker`  
`python -m venv .venv`  
Windows: `.venv\Scripts\activate`  
Linux/macOS: `source .venv/bin/activate`  
`pip install -r requirements.txt`

2. Настройка переменных окружения - создайте `.env` файл:  
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
TELEGRAM_BOT_TOKEN=ваш-токен-бота-телеграм


3. Запустите Redis:  
Windows: `docker run -d -p 6379:6379 redis:alpine`  
Linux/macOS: `sudo service redis-server start`

4. Выполните миграции:  
`python manage.py migrate`

5. Создайте суперпользователя:  
`python manage.py createsuperuser`

6. Запустите сервер и Celery:  
Терминал 1 - Django сервер: `python manage.py runserver`  
Терминал 2 - Celery worker: `celery -A config worker -l info`  
Терминал 3 - Celery beat: `celery -A config beat -l info`

7. Откройте документацию: http://127.0.0.1:8000/swagger/

## 📬 Интеграция с Telegram
1. Создайте бота через @BotFather в Telegram  
2. Скопируйте токен и вставьте в переменную `TELEGRAM_BOT_TOKEN` в `.env`  
3. Найдите своего бота в Telegram и нажмите «Start»  
4. Узнайте свой `chat_id`: https://api.telegram.org/botВАШ_ТОКЕН/getUpdates  
5. Сохраните `chat_id` в профиле пользователя через админку или API  
6. Создайте привычку с временем в будущем — бот пришлёт напоминание!

## 🐳 Docker команды
**Сборка и запуск:**  
`docker compose build` - сборка образов  
`docker compose up` - запуск всех сервисов  
`docker compose up -d` - запуск в фоновом режиме  
`docker compose down` - остановка всех сервисов  

**Выполнение команд в контейнере:**  
`docker compose exec web python manage.py migrate` - миграции  
`docker compose exec web python manage.py createsuperuser` - суперпользователь  
`docker compose exec web python manage.py collectstatic --noinput` - статические файлы  
`docker compose run --rm web python manage.py test` - запуск тестов  

**Просмотр логов:**  
`docker compose logs web -f`  
`docker compose logs celery -f`  
`docker compose logs redis -f`

## 🧪 Тестирование
**Запуск тестов:**  
Локально: `python manage.py test`  
Через Docker: `docker compose run --rm web python manage.py test`  
С покрытием кода:  
`coverage run --source='.' manage.py test`  
`coverage report`

**Проверка качества кода:**  
`flake8 .`  
`python manage.py check`

## 🚀 CI/CD с GitHub Actions
Проект использует автоматический пайплайн развертывания.  
**Workflow stages:** Lint (проверка кода с flake8) → Test (запуск тестов Django) → Build (сборка Docker образа) → Deploy (автоматический деплой на сервер)  

**Требуемые Secrets в GitHub:**  
`DOCKERHUB_USERNAME` - Логин Docker Hub  
`DOCKERHUB_TOKEN` - Токен доступа Docker Hub  
`DEPLOY_SSH_KEY` - Приватный SSH ключ для доступа к серверу  
`SERVER_IP` - IP адрес сервера  
`SSH_USER` - Пользователь для SSH  
`SECRET_KEY` - Секретный ключ Django  
`TELEGRAM_BOT_TOKEN` - Токен Telegram бота  
`DB_NAME` - Имя базы данных  
`DB_USER` - Пользователь БД  
`DB_PASSWORD` - Пароль БД  
`DB_HOST` - Хост БД  

## 📊 Мониторинг
**Проверка статуса контейнеров:**  
`docker compose ps`  
`docker compose logs web -f`  
`docker compose logs celery -f`  
`docker compose logs redis -f`  
`curl http://localhost:8000/api/health/`

## 📁 Структура проекта:
habit_tracker/
├── .github/workflows/deploy.yml # CI/CD пайплайн
├── config/ # Основной проект Django
│ ├── settings.py # Настройки проекта
│ ├── urls.py # Главные URL patterns
│ └── wsgi.py
├── habits/ # Приложение привычек
│ ├── migrations/
│ ├── admin.py # Админка для привычек
│ ├── models.py # Модели Habit, Reward
│ ├── serializers.py # Сериализаторы Django REST
│ ├── tests.py # Тесты приложения
│ ├── urls.py # API endpoints привычек
│ └── views.py # View classes API
├── users/ # Приложение пользователей
│ ├── migrations/
│ ├── admin.py
│ ├── models.py # Модель User
│ ├── serializers.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── telegram_bot/ # Телеграм бот
│ ├── handlers.py # Обработчики команд бота
│ └── tasks.py # Асинхронные задачи
├── docker-compose.yml # Docker Compose конфигурация
├── Dockerfile # Конфигурация Docker образа
├── requirements.txt # Зависимости Python
├── manage.py # Django management script
└── README.md # Документация проекта


## 🔧 Конфигурационные файлы
**Docker Compose сервисы:** web (Django приложение) • celery (Celery worker) • celery_beat (Celery beat) • redis (Брокер сообщений) • db (PostgreSQL база данных)  

**Переменные окружения для продакшн:**  
DEBUG=False
ALLOWED_HOSTS=your-domain.com,ip-address
SECRET_KEY=your-production-secret-key


## 📜 Лицензия
Проект создан в учебных целях. Разрешается использовать код другим лицам с указанием автора.

## 🤝 Разработка
**Добавление новых зависимостей:**  
`pip install новая-зависимость`  
`pip freeze > requirements.txt`  

**Создание миграций:**  
`python manage.py makemigrations`  
`python manage.py migrate`  

**Обновление Docker образа:**  
`docker compose build --no-cache`  
`docker compose up -d`  

---

**Автор**: BaikNadia  
**Версия**: 1.0  
**Последнее обновление**: 2025
