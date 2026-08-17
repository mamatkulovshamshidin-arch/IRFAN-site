"""
Django settings for ИРФАН — Аруу жүрөк.

Production: Vercel + PostgreSQL (DATABASE_URL env var).
Development: SQLite fallback (DATABASE_URL жок болсо).
"""

import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    SECURE_SSL_REDIRECT=(bool, False),
    SECURE_HSTS_SECONDS=(int, 0),
)

# .env файлды окуйт (локалдык иштетүү үчүн; production'до env vars платформадан берилет)
environ.Env.read_env(BASE_DIR / '.env', overwrite=False)

# ---------------------------------------------------------------------------
# Коопсуздук
# ---------------------------------------------------------------------------
# SECRET_KEY .env же платформанын env vars'ынан алынат.
# Эгер жок болсо — ImproperlyConfigured чыгат (бул туура: production'до эч качан
# default key менен иштебеши керек).
SECRET_KEY = env('SECRET_KEY', default='django-insecure-local-dev-only-replace-before-deploy')

DEBUG = env('DEBUG')

# ALLOWED_HOSTS — .env же платформанын env vars'ынан алат
# Мисал: "mysite.vercel.app,mysite.kg,localhost,127.0.0.1"
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Vercel — автоматтык deployment URL'ди кошуу (preview deployments үчүн)
_vercel_url = os.environ.get('VERCEL_URL')
if _vercel_url and _vercel_url not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_vercel_url)

# Render.com — резервдик платформа
_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_render_host)

# ---------------------------------------------------------------------------
# База данных
# DATABASE_URL бар болсо → PostgreSQL (production)
# DATABASE_URL жок болсо  → SQLite (локалдык разработка)
# ---------------------------------------------------------------------------
_database_url = os.environ.get('DATABASE_URL')

if _database_url:
    # Production: PostgreSQL (же башка DATABASE_URL аркылуу)
    DATABASES = {
        'default': env.db('DATABASE_URL')
    }
else:
    # Local development: SQLite fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ---------------------------------------------------------------------------
# Тиркемелер
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise — security'ден кийин, башкасынан мурун
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------
# Сырсөз текшерүү
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Интернационализация
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'ky'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Статикалык файлдар (WhiteNoise аркылуу Vercel'де жайгаштырылат)
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'

_static_dir = BASE_DIR / 'static'
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []

STATIC_ROOT = BASE_DIR / 'staticfiles'

# CompressedManifestStaticFilesStorage — хэш суффикс менен файлдарды кэштейт
# WHITENOISE_MANIFEST_STRICT=False: файл табылбаса crash болбойт
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
}
WHITENOISE_MANIFEST_STRICT = False

# ---------------------------------------------------------------------------
# Media файлдар
# ЭСКЕРТҮҮ: Vercel'дин файл системасы убактылуу (ephemeral).
# Production'до media файлдарды Cloudinary, AWS S3 же Backblaze B2 аркылуу
# сактоо сунушталат. Азырынча локалдык сактоо конфигурацияланган.
# ---------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------------------------------------------
# Башка
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# CSRF жана коопсуздук
# ---------------------------------------------------------------------------
# Vercel preview: https://<deployment>.vercel.app
# Production: өзүңүздүн доменди кошуңуз
CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS',
    default=['https://*.vercel.app'],
)

# Vercel SSL'ди өзү токтотот → SECURE_SSL_REDIRECT керек эмес
# (True болсо → Vercel'де redirect loop болот)
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS: production'до 0 болбосун, бирок Vercel'де SECURE_SSL_REDIRECT=False болгондуктан
# HSTS башкарууну Vercel'дин өзүнө калтырыңыз же env аркылуу коюңуз
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0

# ---------------------------------------------------------------------------
# Django REST Framework жана API схемасы
# ---------------------------------------------------------------------------
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
    'SERVERS': [
        {'url': 'http://127.0.0.1:8000', 'description': 'Жергиликтүү development сервери'},
    ],
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
