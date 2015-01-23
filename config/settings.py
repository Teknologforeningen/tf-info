"""
Django settings for config project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from getenv import env
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Add apps folder to python path.
sys.path.append(os.path.join(BASE_DIR,'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', False)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '.teknologforeningen.fi',
    '.teknolog.fi'
]


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'ordered_model',
    'manager',
    'apps.dagsen',
    'apps.reittiopas',
    'apps.weather',
    'apps.kalender',
    'apps.weathermap',
    'apps.rotatelogos',
    'apps.voteresults'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# https://github.com/kennethreitz/dj-database-url
DATABASES = {'default': dj_database_url.parse(env('DATABASE'))}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'info-cache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'sv-sv'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = env('STATIC_ROOT')

# Media files are the same as static, but meant for file uploads
# Static files are css/JS
MEDIA_URL = '/media/'
MEDIA_ROOT = env('MEDIA_ROOT')

# Filebrowser settings related to MEDIA_ROOT
FILEBROWSER_DIRECTORY = "uploads/"
FILEBROWSER_VERSIONS_BASEDIR = "_versions/"
FILEBROWSER_DEFAULT_PERMISSIONS = 0644

#
# Apps settings
#

# Reittiopas
REITTIOPAS_USER=env('REITTIOPAS_USER')
REITTIOPAS_TOKEN=env('REITTIOPAS_TOKEN')
REITTIOPAS_STOPS=env('REITTIOPAS_STOPS').split(',')

# Kalender
KALENDER_ICAL=env('KALENDER_ICAL')

# IP Camera
CAM_URL=env('CAM_URL')

#Voteresult results
VOTERESULTS_URL=env('VOTE_RESULT')