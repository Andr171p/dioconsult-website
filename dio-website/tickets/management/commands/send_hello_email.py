from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Отпрвка тестового письма"

    def handle(self, *args, **options) -> None:
        self.stdout.write("Отправка письма ...")
        send_mail(
            subject="Welcome subject!",
            message="This is message body! Glad to see you.",
            from_email="admin@admin.com",
            recipient_list=["recipient@example.com"],
            fail_silently=False
        )
        self.stdout.write(self.style.SUCCESS("Письмо отправлено"))
