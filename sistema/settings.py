"""
Django settings for sistema project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-tn78y2+z&k!g^!h14&*ugai-4d#bz*=k4@yzqidrq7er+b+7ha'

DEBUG = True

ALLOWED_HOSTS = []

# ==================================================
# APPS
# ==================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps do projeto
    'app',
    'cadastro',
    'login',
    'painel',
    'carrinho',
    'c_produto',
    'sistema',
]

# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================================================
# URLS
# ==================================================

ROOT_URLCONF = 'sistema.urls'

# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'app' / 'templates',
            BASE_DIR / 'cadastro' / 'templates',
            BASE_DIR / 'login' / 'templates',
            BASE_DIR / 'painel' / 'templates',
            BASE_DIR / 'carrinho' / 'templates',
            BASE_DIR / 'c_produto' / 'templates',
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==================================================
# WSGI
# ==================================================

WSGI_APPLICATION = 'sistema.wsgi.application'

# ==================================================
# DATABASE
# ==================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================================================
# PASSWORDS
# ==================================================

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

# ==================================================
# LANGUAGE
# ==================================================

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = 'static/'

# ==================================================
# MEDIA FILES
# ==================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==================================================
# EMAIL
# ==================================================

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ==================================================
# LOGIN
# ==================================================

LOGIN_REDIRECT_URL = 'painel'
LOGIN_URL = 'login'

# ==================================================
# DEFAULT FIELD
# ==================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'