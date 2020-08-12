"""
Django settings for accountiboard project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from accountiboard import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '07m4jfcu&ejvlu_umu-dm&(qbbhj$o0r8yi60akowb3+abf89a'
JWT_SECRET = 'qZRfj90L5^3bz{pB8[p_H?&nC!W3@V#fLj]O;Nu*/7}P.%Tofp'

ADMINS = [('Iman Shafiei', 'imanshafiei540@gmail.com')]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.DEBUG

SERVER_EMAIL = 'technical@cafeboard.ir'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'technical@cafeboard.ir'
EMAIL_HOST_PASSWORD = 'cafeboard@cafeboard'

ALLOWED_HOSTS = ['*']
MAILER_LIST = ['imanshafiei540@gmail.com']

SMSIR_TOKEN_URL = 'https://RestfulSms.com/api/Token'
SMSIR_ULTRAFAST_SEND_URL = 'https://RestfulSms.com/api/UltraFastSend'
SMSIR_TOKEN_REQUEST = {
    'UserApiKey' : 'fdde10467c6c52bfced9eddf',
    'SecretKey'  : 'YkWWfq8jZkVRqsxp14lVjiNgElWxS9Gz',
}

RECAPTCHA_SITE_KEY   = '6LenhbwZAAAAALB_dr4AvmJyudUMsvSA2rlJkNBm'
RECAPTCHA_SECRET_KEY = '6LenhbwZAAAAAGl4zUfwmXUXqLddrkOM3IANGiaD'


INSTALLED_APPS = [
    'accounti.apps.AccountiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'multiselectfield',
    'corsheaders',
    'compressor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'accountiboard.urls'

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

WSGI_APPLICATION = 'accountiboard.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.DATABASE_NAME,
        'USER': config.DATABASE_USER,
        'PASSWORD': config.DATABASE_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(asctime)s] [%(levelname)s] module: [%(module)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'console_debug_false': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            # But the emails are plain text by default - HTML is nicer
            'include_html': True,
            'filters': ['require_debug_false']
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': 'myapp.log'
        },
        'logfile_info': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': 'myapp_info.log'
        },
        'specific_info': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': 'specific_bug.log'
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': [],
            'propagate': False,
        },
        # Again, default Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['console', 'console_debug_false', 'logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Your own app - this assumes all your logger names start with "myapp."
        'accounti': {
            'handlers': ['logfile'],
            'level': 'WARNING',  # Or maybe INFO or DEBUG
            'propagate': False
        },
        'accounti_info': {
            'handlers': ['logfile_info'],
            'level': 'INFO',  # Or maybe INFO or DEBUG
            'propagate': False
        },
        'specific_bug': {
            'handlers': ['specific_info'],
            'level': 'INFO',  # Or maybe INFO or DEBUG
            'propagate': False
        },
    },
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_TZ = False
TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


PAY_IR_API_KEY = "test"
PAY_IR_REDIRECT_URL = "http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Fpayir%2Fcallback%2F"

# Endpoint for sending requests to get a transaction id.
PAY_IR_API_URL_SEND = 'https://pay.ir/pg/send'
# Bank payment page in which user enters his/her card information for payment.
PAY_IR_API_URL_PAYMENT_GATEWAY = 'https://pay.ir/pg/{token}'
# Verification and committing transactions endpoint.
PAY_IR_API_URL_VERIFY = 'https://pay.ir/pg/verify'