from django.apps import AppConfig


class AiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ai"

    def ready(self):  # noqa: PLR6301
        import ai.signals  # noqa: F401, PLC0415, RUF100, W292
