import os
import logging
import firebase_admin
from firebase_admin import credentials
from pathlib import Path
from dotenv import load_dotenv

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv() 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Initialize environment variables
DEBUG = os.getenv('DEBUG') == 'True'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')


# Email setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Load Firebase configuration from environment variables
firebase_config = {
    "type": os.getenv('F_TYPE'),
    "project_id": os.getenv('F_PROJECT_ID'),
    "private_key_id": os.getenv('F_PRIVATE_KEY_ID'),
    "private_key": os.getenv('F_PRIVATE_KEY'),
    "client_email": os.getenv('F_CLIENT_EMAIL'),
    "client_id": os.getenv('F_CLIENT_ID'),
    "auth_uri": os.getenv('F_AUTH_URI'),
    "token_uri": os.getenv('F_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('F_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('F_CLIENT_X509_CERT_URL'),
}

# Ensure all required environment variables are set
missing_keys = [key for key, value in firebase_config.items() if value is None]
if missing_keys:
    logger.error(f"Missing required environment variables: {', '.join(missing_keys)}")
    raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")

# Replace newline characters in the private key
firebase_config['private_key'] = firebase_config['private_key'].replace('\\n', '\n')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'artworks',
    'users',
    'mail',
    'corsheaders',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.FirebaseAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ALLOWED_ORIGINS = os.getenv('DJANGO_CORS_ALLOWED_ORIGINS', '').split(',')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'ArtBackEnd.urls'

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'https://testartwebapp-gyehawfccpc8gfdt.uksouth-01.azurewebsites.net',
    'https://testartwebappbe.azurewebsites.net',
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'x-requested-with',
]

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

WSGI_APPLICATION = 'ArtBackEnd.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
