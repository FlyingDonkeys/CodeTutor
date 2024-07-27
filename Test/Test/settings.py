"""
Django settings for Test project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

import os
import stripe

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gf2)a)g-4ti)y*vao8#-5jla_(4r!cgep98!f2q-ouzj5_yb_*'
#Google  Maps API Key
GOOGLE_API_KEY = 'AIzaSyC128zZlCt6WN8ygaNo0DtpDi0DL8s0SIM'

#Set up for stripe payment
REDIRECT_DOMAIN = 'http://127.0.0.1:8000'

STRIPE_PUBLIC_KEY_TEST='pk_test_51PREktEZACuDQbJWfonjzkgOmzjX3TS0BmakykrOmeVNbeEpXwVS6O0bX5ZljyWYiGr868iWPZLJCk9LXXx7vmI400i2iA0god'
STRIPE_SECRET_KEY_TEST='sk_test_51PREktEZACuDQbJWu6Jha3n8xccKkaiaHz3JnEuNBtCFvy1LI8HaxadDLnsxeaGM1kb3kY5TtnIG5GtVDhomFEaO008ouzEKwa'
STRIPE_WEBHOOK_SECRET_TEST='whsec_Z0qc7KQvUHU8WyZwEbrc1xc9OlMBOdMZ'

stripe.api_key = STRIPE_SECRET_KEY_TEST 
#test product generated 
PRODUCT_WEEKLY = 'price_1PZT2dEZACuDQbJWOj8wWPR1'
PRODUCT_MONTHLY = 'price_1PZT36EZACuDQbJWR0d2C5Zx'
PRODUCT_YEARLY = 'price_1PZT3fEZACuDQbJWOGybDXvy'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'https://code-tutor-7d77c272e8ff.herokuapp.com',
    '127.0.0.1'
]


# Application definition

INSTALLED_APPS = [
    'CodeTutor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
]

ROOT_URLCONF = 'Test.urls'

AUTH_USER_MODEL = 'CodeTutor.CommonUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Test.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/



# This line should be added to define where static files will be collected

STATIC_URL = '/CodeTutor/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'CodeTutor/static/CodeTutor/images/'),
    os.path.join(BASE_DIR, 'CodeTutor/static/CodeTutor/javascript/')
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
