"""
Using Django 2.2.7.
"""

import os
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6uq30fk9ozqtq&!&0qf4i24@dz_8-xj08iixb402z@e6o_soug'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.environ.get("DEBUG", False) == "False" else True

# Adds noindex tag to the template
ALLOW_BOTS = False

ALLOWED_HOSTS = [
    'brandpulsar.com',
    '157.230.19.185'
]

# STRIPE_SECRET_KEY="sk_test_CPDJaW3ubEBaR50ggcvwnXZ400XxjfAcvs"
# STRIPE_PUBLISHABLE_KEY="pk_test_wmAGRMcQtiJ2u8pPr3Adg2mv00e7iErr6z"

# TEST WEBHOOKS

# STRIPE_INSTALMENT_WEBHOOK_ENPOINT_SECRET = 'whsec_QXop9bZRnUQsLZAeu3PcybDICFuqiJKw'
# STRIPE_FEATURED_WEBHOOK_ENPOINT_SECRET = 'whsec_as9fTEjKmuVEA0V9B0SqnRWR8nsNQ30N'

STRIPE_SECRET_KEY = 'sk_live_1a7XYNLaSJlRifq959qgGUUa00raNTCsge'
STRIPE_PUBLISHABLE_KEY = 'pk_live_3gD4r9HPQSJhjA9gwpfllJNF00T8vxHnYi'

# LIVE WEBHOOKS

STRIPE_INSTALMENT_WEBHOOK_ENPOINT_SECRET = 'whsec_QXop9bZRnUQsLZAeu3PcybDICFuqiJKw'
STRIPE_FEATURED_WEBHOOK_ENPOINT_SECRET = 'whsec_ix4J4i2vlIMH0mV3A8tXHgrHRqs1uMaS'

BASE_URL = 'https://brandpulsar.com'

# BASE_URL = 'http://127.0.0.1:8000'

MAILCHIMP_USERNAME = 'cosmicdomain'
MAILCHIMP_API_KEY = '58b2fca9e381d5f2b4f47f3612cd93cb-us19'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    # 'channels',
    'main',
    'ckeditor',
    'ckeditor_uploader',
    'mathfilters',
    'django_filters',
    'rest_framework',
    'treebeard',
    'pagination_bootstrap',
    'users',
    'marketplace',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
]

ROOT_URLCONF = 'brandpulsar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.allow_bots',
                'main.context_processors.faqs_processor',
                'main.context_processors.industries_processor',
            ],
        },
    },
]

#WSGI_APPLICATION = 'cosmicdomain.wsgi.application'
ASGI_APPLICATION = "cosmicdomain.routing.application"

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [(
#                 os.environ.get('REDIS_HOST', 'localhost'),
#                 os.environ.get('REDIS_PORT', 6379)
#             )],
#         },
#     },
# }

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB", "cosmicdomain"),
        'USER': os.environ.get("POSTGRES_USER", "cosmicdomainuser"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "icui4cu"),
        'HOST': os.environ.get("POSTGRES_HOST", "localhost"),
        'PORT': os.environ.get("POSTGRES_PORT", 5432)
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'brandpulsar/static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media-root")

CKEDITOR_UPLOAD_PATH = 'media/ckeditor_uploads/'

SENDGRID_API_KEY = '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'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

AUTH_USER_MODEL = 'users.User'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 24,
}


# Celery settings
# https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html


# CELERY_BROKER_URL = os.environ.get(
#     "BROKER_URL", "redis://:1qvSgjrAIRAHqD2ZqdV1Ojzxw@localhost:6379/0"
# )

# CELERY_TASK_IGNORE_RESULT = True
# CELERY_TIMEZONE = TIME_ZONE


# Login url
LOGIN_URL = reverse_lazy('users:login-view')


# GoDaddy API Credentials
GODADDY_KEY = "dKiSnBoQsS47_XBZVJsJBisPPy7DEQGzYp2"
GODADDY_SECRET = "H1zWjPNVVustMgntHV58KQ"


# Date input forms
DATE_INPUT_FORMATS = ['%d-%m-%Y']


# Google OAUTH CREDENTIALS
GOOGLE_OAUTH_CLIENT_ID = "883270625790-i1rf30v76so056s1jjsjijivi4kc56tn.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET = "Cvr_3cfbAQRu5oYcrbhDycR5"
