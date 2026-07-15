import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent


class Config:
    def __init__(self):
        self._validate_required()

        self.DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        allowed_hosts_raw = os.getenv('ALLOWED_HOSTS', '')
        self.ALLOWED_HOSTS = allowed_hosts_raw.split(',') if allowed_hosts_raw else []
        csrf_raw = os.getenv('CSRF_TRUSTED_ORIGINS', '')
        self.CSRF_TRUSTED_ORIGINS = csrf_raw.split(',') if csrf_raw else []
        self.HOST_URL = os.getenv('HOST_URL', 'http://localhost:8000')
        self.DATABASE = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ.get('DB_NAME', ''),
                'USER': os.environ.get('DB_USER', ''),
                'PASSWORD': os.environ.get('DB_PASS', ''),
                'HOST': os.environ.get('DB_HOST', 'localhost'),
                'PORT': os.environ.get('DB_PORT', '5432'),
            }
        }
        self.EMAIL_HOST = os.getenv('EMAIL_HOST', '')
        self.EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
        self.EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
        self.EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
        self.EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
        self.EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes')
        self.DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', '')
        admins_raw = os.getenv('ADMINS', '')
        self.ADMINS = self._parse_admins(admins_raw) if admins_raw else []

        self.REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

        self.YOOKASSA_SHOP_ID = os.getenv('YOOKASSA_SHOP_ID', '')
        self.YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY', '')

    def _validate_required(self):
        required_if_prod = [
            'SECRET_KEY',
        ]
        for var_name in required_if_prod:
            value = os.getenv(var_name)
            if not value:
                raise RuntimeError(
                    f"Required environment variable '{var_name}' is not set. "
                    f"Please check your .env file."
                )

    @staticmethod
    def _parse_admins(admins_str: str) -> list:
        """Parse ADMINS string into Django format: [('Name', 'email@domain.com'), ...]"""
        result = []
        parts = [p.strip() for p in admins_str.split(',') if p.strip()]
        for part in parts:
            if '@' in part:
                result.append(('Admin', part))
            else:
                result.append((part, part))
        return result


config = Config()
