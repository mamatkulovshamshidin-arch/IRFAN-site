from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
# .env файлы болсо окуйт, болбосо environment variables'дан алат
environ.Env.read_env(BASE_DIR / '.env', overwrite=False)
SECRET_KEY = env('SECRET_KEY', default='django-insecure-build-only-replace-in-production-env')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Render.com — автоматтык hostname кошуу
import os
RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)

# Vercel — автоматтык hostname кошуу
VERCEL_URL = os.environ.get('VERCEL_URL')
if VERCEL_URL:
    ALLOWED_HOSTS.append(VERCEL_URL)

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'drf_spectacular',
    'core',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': [
    'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]}}]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': env.db(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE = 'ky'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
# STATICFILES_DIRS — staticfiles папкасы жок болсо crash болбосун
_static_dir = BASE_DIR / 'static'
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'ИРФАН — Аруу жүрөк API',
    'DESCRIPTION': (
        '«Аруу жүрөк» диний-агартуу курсунун ачык REST API документациясы.\n\n'
        '**Пагинация:** Тизме жооптору `{ count, next, previous, results }` форматында кайтарылат.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {'name': 'ИРФАН диний уюму', 'email': 'irfanreligiousorg@gmail.com'},
    'SERVERS': [{'url': 'http://127.0.0.1:8000', 'description': 'Жергиликтүү development сервери'}],
    'TAGS': [
        {'name': 'Окуу багыттары', 'description': 'Диний-агартуу курсунун багыттары'},
        {'name': 'Мугалимдер',    'description': 'Курстун мугалимдери жана устаздары'},
        {'name': 'Сабактар',      'description': 'Окуу программасындагы сабактар'},
        {'name': 'Жаңылыктар',   'description': 'Уюмдун жаңылыктары жана макалалары'},
        {'name': 'FAQ',           'description': 'Көп берилүүчү суроолор жана жооптор'},
    ],
    'COMPONENT_SPLIT_REQUEST': False,
    'SORT_OPERATIONS': False,
}
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=not DEBUG)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0 if DEBUG else 31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
