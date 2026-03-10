import os

from dotenv import load_dotenv

from .base import *

load_dotenv()
# -------------------------------
# РАЗРАБОТКА — локальный запуск
# -------------------------------

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "*"]

# Секретный ключ можно захардкодить локально (или оставить через .env)
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
# Отправка писем в консоль

# === УБИРАЕМ ТО, ЧТО МЕШАЕТ ЛОКАЛЬНО ===

# 1. Убираем WhiteNoise из middleware (он нужен только в проде)
MIDDLEWARE = [m for m in MIDDLEWARE if m != "whitenoise.middleware.WhiteNoiseMiddleware"]

# 2. Отключаем ManifestStaticFilesStorage (он ломается без collectstatic)
if "ManifestStaticFilesStorage" in str(STORAGES["staticfiles"]):
    STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.StaticFilesStorage"

# 3. Подключаем локальные переопределения (если есть .local.py)
try:
    from .local import *
except ImportError:
    pass
