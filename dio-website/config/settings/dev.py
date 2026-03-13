import os

from .base import *
# -------------------------------
# РАЗРАБОТКА — локальный запуск
# -------------------------------

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "*"]

# Секретный ключ можно захардкодить локально (или оставить через .env)
SECRET_KEY = os.getenv("SECRET_KEY", "dvanbirgcdamkpm")

MAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

if DEBUG:
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1027

# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "noreply@example.com"
SERVER_EMAIL = os.getenv("SERVER_EMAIL")
FASTAPI_RAG = os.environ.get("FASTAPI_RAG")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN")

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
