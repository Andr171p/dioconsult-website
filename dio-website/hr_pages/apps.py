from django.apps import AppConfig


class HrConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hr_pages"

    def ready(self):  # noqa: PLR6301
        import hr_pages.wagtail_hooks  # noqa: F401, PLC0415, RUF100, W292
