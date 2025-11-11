import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Force using Redis from environment variable
import os
redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
app.conf.broker_url = redis_url
app.conf.result_backend = redis_url

print(f"Celery configured with broker: {app.conf.broker_url}")

# Optional configuration
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.timezone = 'UTC'
app.conf.enable_utc = True
