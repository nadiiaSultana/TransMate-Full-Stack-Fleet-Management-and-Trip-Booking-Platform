from pathlib import Path
from datetime import timedelta
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='django-insecure-transmate-dev-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'rest_framework','rest_framework_simplejwt','corsheaders',
    'apps.users','apps.vehicles','apps.bookings','apps.trips','apps.payments','apps.ratings','apps.complaints','apps.notifications','apps.reports','apps.maintenance',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[],
    'APP_DIRS':True,
    'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']},
}]
WSGI_APPLICATION = 'config.wsgi.application'

DB_ENGINE = config('DB_ENGINE', default='django.db.backends.sqlite3')
if DB_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {'default': {'ENGINE': DB_ENGINE, 'NAME': BASE_DIR / config('DB_NAME', default='db.sqlite3')}}
else:
    DATABASES = {'default': {'ENGINE': DB_ENGINE,'NAME': config('DB_NAME', default='transmate_db'),'USER': config('DB_USER', default='postgres'),'PASSWORD': config('DB_PASSWORD', default='postgres'),'HOST': config('DB_HOST', default='localhost'),'PORT': config('DB_PORT', default='5432')}}

AUTH_USER_MODEL = 'users.User'
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}
SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),'REFRESH_TOKEN_LIFETIME': timedelta(days=7),'AUTH_HEADER_TYPES': ('Bearer',)}

BKASH_BASE_URL = config('BKASH_BASE_URL', default='https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout')
BKASH_APP_KEY = config('BKASH_APP_KEY', default='')
BKASH_APP_SECRET = config('BKASH_APP_SECRET', default='')
BKASH_USERNAME = config('BKASH_USERNAME', default='')
BKASH_PASSWORD = config('BKASH_PASSWORD', default='')
NAGAD_BASE_URL = config('NAGAD_BASE_URL', default='')
NAGAD_MERCHANT_ID = config('NAGAD_MERCHANT_ID', default='')
NAGAD_MERCHANT_PRIVATE_KEY = config('NAGAD_MERCHANT_PRIVATE_KEY', default='')
NAGAD_PG_PUBLIC_KEY = config('NAGAD_PG_PUBLIC_KEY', default='')
FRONTEND_PAYMENT_SUCCESS_URL = config('FRONTEND_PAYMENT_SUCCESS_URL', default='http://localhost:5173/payment/success')
FRONTEND_PAYMENT_FAIL_URL = config('FRONTEND_PAYMENT_FAIL_URL', default='http://localhost:5173/payment/fail')
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='TransMate <noreply@transmate.local>')
