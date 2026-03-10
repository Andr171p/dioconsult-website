import os
from pathlib import Path

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
BASE_DIR = Path(BASE_DIR) if isinstance(BASE_DIR, str) else BASE_DIR
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
MAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").strip().lower() == "true"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False").strip().lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL")
FASTAPI_RAG = os.environ.get("FASTAPI_RAG")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment variables!")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Security settings
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False  # Nginx будет обрабатывать SSL
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database - ИСПРАВЛЕННЫЙ ПУТЬ
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # Используем pathlib
    }
}

# Static files
STATIC_ROOT = BASE_DIR / "static"  # pathlib стиль
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"  # pathlib стиль
MEDIA_URL = "/media/"

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = (
    "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
)

try:
    from .local import *
except ImportError:
    pass
