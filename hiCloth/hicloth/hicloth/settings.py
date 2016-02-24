"""
Django settings for hicloth project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.core.exceptions import ImproperlyConfigured


def get(key):
    from django.conf import settings

    defaults = {
        'LOGIN_AFTER_REGISTRATION': True,
        'LOGIN_AFTER_ACTIVATION': True,
        'SEND_ACTIVATION_EMAIL': False,
        'SET_PASSWORD_RETYPE': False,
        'SET_USERNAME_RETYPE': False,
        'PASSWORD_RESET_CONFIRM_RETYPE': False,
    }
    defaults.update(getattr(settings, 'DJOSER', {}))
    try:
        return defaults[key]
    except KeyError:
        raise ImproperlyConfigured(
            'Missing settings: DJOSER[\'{}\']'.format(key))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pxe$dcdbh=)0)j3p689l4q9u=jk4-oko$5jojsb51&yz^mv*ug'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest',
    'rest_framework',
    'rest_framework.authtoken',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hicloth.urls'

WSGI_APPLICATION = 'hicloth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hicloth',
        'USER': 'hicloth',
        'PASSWORD': '872505651CL)TH',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Iran'

USE_I18N = True

USE_L10N = True

#USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

#
# APPEND_SLASH = False
#
# SMART_APPEND_SLASH = True

# SERVER_IP_PORT = 'http://188.166.109.225:8080/'
# SERVER_IP_PORT = 'http://91.98.103.222:8080/'
SERVER_IP_PORT = 'http://127.0.0.1:8000/'
