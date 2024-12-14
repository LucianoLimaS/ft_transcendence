"""
Django settings for ft_transcendence project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY','change-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',')
    if h.strip()
]

# Usando o model customizado de usuário
AUTH_USER_MODEL = "users.Users"

# Application definition

WSGI_APPLICATION = 'ft_transcendence.wsgi.application'

ASGI_APPLICATION = 'ft_transcendence.asgi.application'

INSTALLED_APPS = [
    'channels',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.custom_auth',
    'apps.chat',
    'apps.badges',
    'apps.match',
    'apps.tournaments',
    'apps.users',
    'django_prometheus',
    'django_htmx',
    'django_redis',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

# Definindo as rotas para expor as métricas
PROMETHEUS_METRICS_EXPORT_ENDPOINT = '/metrics'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # Substitua pelo endereço correto do seu Redis
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",  # Certifique-se de que esta classe está correta
        }
    }
}


ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'ft_transcendence.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'apps' / 'common_templates',             # Diretório para templates base
            BASE_DIR / 'apps' / 'chat' / 'templates',           # Templates do chat
            BASE_DIR / 'apps' / 'badges' / 'templates',         # Templates do badges
            BASE_DIR / 'apps' / 'custom_auth' / 'templates',    # Templates do custom_auth
            BASE_DIR / 'apps' / 'match' / 'templates',          # Templates do match
            BASE_DIR / 'apps' / 'tournaments' / 'templates',    # Templates do tournaments
            BASE_DIR / 'apps' / 'users' / 'templates',          # Templates do users
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.users.context_processors.minio_settings',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Backend padrão
    'apps.custom_auth.backends.CustomAuthBackend'
    # Adicione outros backends personalizados, se necessário
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django_prometheus.db.backends.postgresql'),
        'NAME': os.getenv('POSTGRES_DB', 'transcendence'),
        'USER': os.getenv('POSTGRES_USER', 'transcendence'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'transcendence'),
        'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = [
        ('en', _('English')),
        ('es', _('Spanish')),
        ('pt-br', _('Portuguese (Brazil)')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

CSRF_TRUSTED_ORIGINS = ['https://localhost', 'http://127.0.0.1:8000']

STATIC_URL = '/static/'

# # Diretório para arquivos estáticos após o collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Certifique-se que esse caminho existe
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'apps/custom_auth/custom_static'),  # Caminho correto para custom_auth
    os.path.join(BASE_DIR, 'apps/match/static'),         # Exemplo para o app match, adicione conforme necessário
    os.path.join(BASE_DIR, 'apps/users/static'),         # Exemplo para o app users
    os.path.join(BASE_DIR, 'apps/badges/static'),        # Exemplo para o app badges
    os.path.join(BASE_DIR, 'apps/chat/static'),          # Exemplo para o app chat
    os.path.join(BASE_DIR, 'apps/tournaments/static'),    # Exemplo para o app tournaments
    os.path.join(BASE_DIR, 'apps/static'),                # Se houver um diretório estático global
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

EMAIL_API_KEY = os.getenv('EMAIL_API_KEY', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')

from django.contrib.messages import constants

MESSAGE_TAGS = {
    constants.DEBUG: 'alert-primary',
    constants.INFO: 'alert-info',
    constants.SUCCESS: 'alert-success',
    constants.WARNING: 'alert-warning',
    constants.ERROR: 'alert-danger',
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],  # O nome do serviço e a porta do Redis
        },
    },
}

LOGIN_URL = '/'  # Já que o login é na URL base
LOGIN_REDIRECT_URL = '/'  # Ou o nome da URL do chat

MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "access-key")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "secret-key")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET", "my-local-bucket")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "my-local-bucket")
MINIO_EXTERNAL_ENDPOINT = os.getenv("MINIO_EXTERNAL_ENDPOINT", "http://localhost:9002")