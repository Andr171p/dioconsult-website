from django.apps import AppConfig


class VacancyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vacancy"

    def ready(self):  # noqa: PLR6301
        import vacancy.wagtail_hooks  # noqa: F401, PLC0415, RUF100, W292
