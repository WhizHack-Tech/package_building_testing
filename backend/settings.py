"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

#  ==================================================================================================================================================================================================================================================
#  File Name: settings.py
#  Description: XDR_Backend project's settings file to include all the configurations required for the django project like: database configurations, list of all installed apps in the project, Html template path, SMTP credentials, Debug mode etc.

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ==================================================================================================================================================================================================================================================

from pathlib import Path
import os
import psycopg2
import psycopg2.extensions
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR_html = Path().resolve()
DASHBOARD_DIR = os.path.join(BASE_DIR, '../frontend_master')
# BACKEND_TEMPLATE = os.path.join(BASE_DIR, '../Master_backEnd/templates')
BACKEND_TEMPLATE = os.path.join(BASE_DIR_html, 'templates/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
 
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y3)h!u0#xg4-9hst@!&dzd6uz&93hf==tmklbu(p5mebpd6a!w'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

# ALLOWED_HOSTS = ['*', '3.210.183.86', 'localhost','127.0.0.1']
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'backend_app',    
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [DASHBOARD_DIR,BACKEND_TEMPLATE],
        'DIRS': [BACKEND_TEMPLATE,os.path.join(BASE_DIR, '../backend_app')],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database config live postgresql
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'testing_live_db2',
        # Local User name & Password
        ##########################################################
        # 'USER': 'postgres',
        # 'PASSWORD': 'Ancient8-Outpour-Freemason-Pancreas',
        ##########################################################
        # Online User name & Password
        ##############################3###########################
        'USER': 'postgres',
        'PASSWORD': 'Ancient8-Outpour-Freemason-Pancreas',
        ##########################################################
        # Local Host & Port
        # 'HOST': 'ec2-3-145-61-145.us-east-2.compute.amazonaws.com',
        # 'PORT': 5432,
        ##########################################################
        # Online Host & Port
        'HOST': <<DATABASE-HOST>>,
        'PORT': 5432,
        ###########################################################
        'OPTIONS':{
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        }
     }
 }
 
# Database config local postgresql
""" DATABASES = {
     'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "zh_db",
        'USER': "postgres",
        'PASSWORD': "12345",
        'HOST': "localhost",
        'PORT': "5432",
        'OPTIONS':{
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        }
     }
 } """

 # Database config local sqllite
""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} """



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


#simple jwt 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

# SIMPLE_JWT config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),    
}

AUTH_USER_MODEL = 'backend_app.User'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher',]


#To store the image in static folder
# STATIC_URL = '/static/'
# MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, ''),
    # BASE_DIR / 'static'

]

#MEDIA_ROOT = 'static/images'

STATIC_URL = '/static/'
MEDIA_URL = '/image/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/image')		

# SMTP Settings Gmail
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = "noreply@whizhack.com"
EMAIL_HOST_PASSWORD = "Whenever@Shorty@8rink"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# s3 bucket credentials
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'AKIAV5DTNCS2ZOACWF53'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 's3-xdrdashboardimages'
# AWS_QUERYSTRING_AUTH = False

