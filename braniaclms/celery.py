import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'braniaclms.settings')  # Путь к файлу основных настроек
celery_app = Celery('braniac')  # Название Celery приложения и его идентификатор
celery_app.config_from_object('django.conf.settings', namespace='CELERY')   # Указание на то, откуда будут подтягиваться остальные настройки
celery_app.autodiscover_tasks() # Автообработка задачь