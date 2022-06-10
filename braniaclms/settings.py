"""
Django settings for braniaclms project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv # работа с виртуальным окружением подкладывай файлик .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import django.core.mail.backends.filebased
import django_redis.cache

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y*h(5l20b)7@gl1*=7)=*r45oo-jkl25lvk-3+8yrz%zxh@@cz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DEBUG') == 'True' else False

ALLOWED_HOSTS = ['*']

ENV_TYPE = os.getenv('ENV_TYPE', 'prod')

if DEBUG:
    INTERNAL_IPS = [
        "192.168.1.4",
        "127.0.0.1",
    ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'markdownify.apps.MarkdownifyConfig',
    'social_django',
    'authapp',
    'mainapp',
    'crispy_forms',
    'debug_toolbar',
    'seeding',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Обработка интернационализации
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'braniaclms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'braniaclms.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if ENV_TYPE == 'local':

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'lms',
            'USER': 'postgres'
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'     # задает "домашнюю" языковую зону

TIME_ZONE = 'UTC'           # задает "домашнее" время

USE_I18N = True             # дает возможность использовать интренацианализацию

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
if ENV_TYPE == 'local':
    # Работа со статикой локально
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
else:
    # Работа со статикой на сервере
    STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SEEDING_DIR = "mainapp/seeding"

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'authapp.CustomUser'
LOGIN_REDIRECT_URL = 'mainapp:main_page'
LOGOUT_REDIRECT_URL = 'mainapp:main_page'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GITHUB_KEY = os.getenv("GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("GITHUB_SECRET")

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'

# Отправка сообщений в реальных проектах(настройки указываются в документации sntp-сервера)
# Настройка позволяет выслать 500-е ошибки на указанный адрес при DEBUG = False
# Используй!

# ADMINS = (
#     ('myemail@email.com', 'ilya')
# )

# EMAIL_HOST = 'sntp.yandex.ru'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'myname@yandex.ru'
# EMAIL_HOST_PASSWORD = 'mypassword'
# EMAIL_USE_SSL = True

# Отправка сообщений для учебного проекта
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'emails-tmp'

# LOG_FILE = BASE_DIR / 'log' / 'myapp_log.log'
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             'format': '[%(asctime)s] %(levelname)s %(name)s (%(lineno)d) %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console'
#         },
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': LOG_FILE,   # Не забудь создать папку log
#             'formatter': 'console',
#         },
#     },
#     'loggers': {
#         'django': {
#             'level': 'INFO',
#             'handlers': ['file', 'console']
#         },
#     },
# }
# Определение путей для локализаций
# затем в консоли python3 manage.py makemessages -l ru -i venv
LOCALE_PATHS = [BASE_DIR / 'locale']
