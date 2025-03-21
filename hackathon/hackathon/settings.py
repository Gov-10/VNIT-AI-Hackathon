"""
Django settings for hackathon project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# from pathlib import Path
# import os
# from dotenv import load_dotenv
# import dj_database_url
# import environ

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'your-railway-app-url.up.railway.app']

# # Application definition
# INSTALLED_APPS = [
#     'corsheaders',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'myHackathon',  # Added your app
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',  # Added CORS middleware
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#      'whitenoise.middleware.WhiteNoiseMiddleware'
# ]

# # CORS Settings
# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:8000"
# ]  # Allow API requests from any origin (change in production)

# CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000" , 'https://your-railway-app-url.up.railway.app']

# ROOT_URLCONF = 'hackathon.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Added templates directory
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'hackathon.wsgi.application'

# env = environ.Env()
# environ.Env.read_env()
# # Database
# DATABASES = {
#     'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'myHackathon/static')]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # Collects all static files here

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DATABASES = {
#     'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
# }

# DEBUG = os.getenv("DEBUG", "False") == "True"

# INSTALLED_APPS += ['whitenoise.runserver_nostatic']
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# # Use WhiteNoise for static file handling
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"






from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import environ

# Load environment variables
load_dotenv()

env = environ.Env()
environ.Env.read_env()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Debug mode
DEBUG = os.getenv("DEBUG", "False") == "True"

# Allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'vnit-ai-hackathon-production.up.railway.app']

# Installed apps
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myHackathon',  # Your app
    'whitenoise.runserver_nostatic',  # WhiteNoise for static files
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added before other middlewares
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = False  # Change from True to False

CORS_ALLOWED_ORIGINS = [
    "https://vnit-ai-hackathon-production.up.railway.app",
    "http://127.0.0.1:8000",  # Add this if testing locally
]

CSRF_TRUSTED_ORIGINS = [
    "https://vnit-ai-hackathon-production.up.railway.app",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS"
]
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = None

CORS_ALLOW_CREDENTIALS = True
# URL configurations
ROOT_URLCONF = 'hackathon.urls'

# Templates
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
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'hackathon.wsgi.application'

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'railway', 'USER': 'postgres' , 'PASSWORD': 'WkSuoYpIzpcKyFXYHIQpSOZNGSddGEJC', 'HOST' : 'postgres.railway.internal', 'PORT':'5432',}}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'myHackathon/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# WhiteNoise for static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

