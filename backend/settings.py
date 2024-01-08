"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
#  ==================================================================================================================================================================================================================================================
#  File Name: settings.py
#  Description: XDR_Backend project's settings file to include all the configurations required for the django project like: database configurations, list of all installed apps in the project, Html template path, SMTP credentials, Debug mode etc.

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ==================================================================================================================================================================================================================================================

import os
from configparser import ConfigParser
from datetime import timedelta
from pathlib import Path

import psycopg2
import psycopg2.extensions

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR_html = Path().resolve()
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "./backend/config.ini")
REPORT_PATH = os.path.join(BASE_DIR, "../backend/media")
BACKEND_TEMPLATE = os.path.join(BASE_DIR_html, "templates/")

# Read config.ini file
config_object = ConfigParser()
# Localhost
# config_object.read("C://Users//WhizEmp0030//Documents//GitHub//django_react//backend//backend//config.ini")
config_object.read(CONFIG_FILE_PATH)
# Onlinehost
# config_object.read('/app/backend/backend/config.ini')
# Get the all info

userinfo = config_object["USERINFO"]
# Write changes back to file localhost
# with open('C://Users//WhizEmp0030//Documents//GitHub//django_react//backend//backend//config.ini', 'w') as conf:
with open(CONFIG_FILE_PATH, "w") as conf:
    config_object.write(conf)
    # Onlinehost
# with open('/app/backend/backend/config.ini','w') as conf:
# config_object.write(conf)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c%t!4yb!z1qy8*yhh)zd4lts5u*_^o_sw)5idw@5=j%cbfu$wk"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

ALLOWED_HOSTS = [
    "*",
    "3.210.183.86",
    "localhost",
    "127.0.0.1",
    "https://xdr.zerohack.in/",
    "https://dev-xdr.zerohack.in",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "frontend",
    "corsheaders",
    "channels",
]

ASGI_APPLICATION = "backend.asgi.application"

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

CHANNELS_WS_PROTOCOL_TIMEOUT = 10

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
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

ROOT_URLCONF = "backend.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BACKEND_TEMPLATE, os.path.join(BASE_DIR, "../frontend")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# Database config live postgresql
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "testing_live_db12",
        "USER": "postgres",
        "PASSWORD": "Ancient8-Outpour-Freemason-Pancreas",
        "HOST": "172.16.2.75",
        "PORT": 5432,
        "OPTIONS": {
            "isolation_level": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
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
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR_html, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR_html, "static")

STATIC_URL = "api/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# print(CACHES)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DATE_INPUT_FORMATS": ["%Y-%M-%D-%H-%M-%S"],
}

# SIMPLE_JWT config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=120),
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
}

AUTH_USER_MODEL = "frontend.Client_data"
USER_ID_FIELD = "id"

# SMTP Settings Gmail
EMAIL_HOST = "smtp.office365.com"
EMAIL_HOST_USER = "noreply@whizhack.com"
EMAIL_HOST_PASSWORD = "Whenever@Shorty@8rink"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

AWS_ACCESS_KEY_ID = "AKIAV5DTNCS2ZOACWF53"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "s3-xdrdashboardimages"
