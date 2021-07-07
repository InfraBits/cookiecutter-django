"""
Django settings for {{ cookiecutter.project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

from {{ cookiecutter.project_name }}.utils import load_config

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG = load_config(BASE_DIR)

SECRET_KEY = CONFIG["django"]["secret_key"]
DEBUG = CONFIG["django"]["debug"]
ALLOWED_HOSTS = CONFIG["django"]["allowed_hosts"]
ADMINS = CONFIG["django"]["admins"]

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
{%- if cookiecutter.celery_worker == 'y' %}
    'django_celery_results',
    'django_celery_beat',
{%- endif %}
    'django_probes',
    '{{ cookiecutter.project_name }}.{{ cookiecutter.project_name }}',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = '{{ cookiecutter.project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{{ cookiecutter.project_name }}.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": CONFIG["mysql"]["name"],
        "HOST": CONFIG["mysql"]["host"],
        "USER": CONFIG["mysql"]["user"],
        "PASSWORD": CONFIG["mysql"]["password"],
    }
}

{%- if cookiecutter.celery_worker == 'y' %}
CELERY_BROKER_URL = CONFIG["redis"]["url"]
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
{%- endif %}

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

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}
else:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

    CSP_REPORT_ONLY = CONFIG["csp"].get("report_only", False)
    CSP_DEFAULT_SRC = CONFIG["csp"].get("default_src", "'self'")
    CSP_BLOCK_ALL_MIXED_CONTENT = CONFIG["csp"].get("block_all_mixed_content", True)

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_SANDBOX_MODE_IN_DEBUG = True
SENDGRID_API_KEY = CONFIG["sendgrid"]["api_key"]
