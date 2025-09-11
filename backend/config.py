import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent


class Config:
    DEBUG = os.getenv('DEBUG', False)
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(',')
    HOST_URL = os.getenv('HOST_URL')
    DATABASE = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', "True").lower() == "true"
    EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', "False").lower() == "true"
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
    ADMINS = os.getenv('ADMINS')

    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

    YOOKASSA_SHOP_ID = os.getenv('YOOKASSA_SHOP_ID')
    YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY')


config = Config()
