"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY_DJANGO')

# SECURITY WARNING: don't run with debug turned on in production!
# production.pyでDEBUG = Falseになっている為、↓がどちらになっていても本番環境ではデバッグがFalseになる。
DEBUG = True

ALLOWED_HOSTS = ["https://toyo-university-ym-iniad-7gxwnlu9c4g7wrim.onrender.com", "https://toyo-university-ym079-iniad.onrender.com", "127.0.0.1", 'localhost']


# Application definition

INSTALLED_APPS = [
    'intern',
    'weather',
    'accounts',
    'auther',
    'chatGPT',
    'social_django',
    'game',
    'mymath',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
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

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 6
AXES_RESET_ON_SUCCESS=True
AXES_LOCKOUT_PARAMETERS = ["username"]
AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = False
AXES_LOCKOUT_TEMPLATE = 'accounts/lock.html'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('MAIL')
EMAIL_HOST_PASSWORD = os.getenv('APP_PASS')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER_RE = os.getenv('MAIL_RE')
HANDLER404 = 'chatGPT.views.rate_limit_exceeded'

# ログアウトまでの時間 (秒)
SESSION_COOKIE_AGE = 60 * 60 * 24
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'carzone/static')]

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'intern:index'
LOGOUT_REDIRECT_URL = 'accounts:login' 


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

OPEN_WEATHER_API = os.getenv('OPEN_WEATHER_API')
OPEN_AI_API = os.getenv('OPEN_AI_API')
OPEN_AI_URL = os.getenv('OPEN_AI_URL')

OPEN_AI_API_MY = os.getenv('OPEN_AI_API_MY')
OPEN_AI_URL_MY = os.getenv('OPEN_AI_URL_MY')