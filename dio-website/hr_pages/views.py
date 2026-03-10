from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .forms.vacancy import VacancyForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models.vacansy import Vacancy
# vacancy/views.py — добавь в конец
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def latest_unprocessed_vacancy(request):
    vacancy = Vacancy.objects.filter(is_processed=False).order_by('-created_at').first()
    if vacancy:
        return JsonResponse({'id': vacancy.id})
    return JsonResponse({'id': None})



@staff_member_required
def vacancy_unprocessed_count(request):
    count = Vacancy.objects.filter(is_processed=False).count()
    return JsonResponse({"count": count})



@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@authentication_classes([])
@permission_classes([])
def vacancy_view(request):
    form = VacancyForm(request.data, request.FILES)
    
    if form.is_valid():
        vacancy = form.save()
        
        try:
            subject = f'Новое резюме: {vacancy.name} - {vacancy.title}'
            
            # HTML шаблон письма
            html_message = render_to_string('vacancy/email_template.html', {
                'vacancy': vacancy,
            })
            
            # Текстовая версия
            plain_message = f"""
НОВОЕ РЕЗЮМЕ

Имя: {vacancy.name}
Телефон: {vacancy.phone}
Вакансия: {vacancy.title}
Дата: {vacancy.created_at.strftime("%d.%m.%Y %H:%M")}

📎 Резюме: {vacancy.resume.name if vacancy.resume else "Не прикреплено"}
🔗 Ссылка для скачивания: {vacancy.resume_link if vacancy.resume_link else "Нет"}

--
Отправлено автоматически с сайта
            """
            
            # Создаем email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.EMAIL_HOST_USER],
            )
            
            # Добавляем HTML версию
            email.attach_alternative(html_message, "text/html")
            
            # Добавляем файл резюме если есть
            if vacancy.resume and os.path.exists(vacancy.resume.path):
                try:
                    with open(vacancy.resume.path, 'rb') as file:
                        email.attach(
                            filename=vacancy.resume.name,
                            content=file.read(),
                            mimetype='application/octet-stream'
                        )
                    print(f"Файл резюме прикреплен: {vacancy.resume.name}")
                except Exception as file_error:
                    print(f"Не удалось прикрепить файл: {file_error}")
            
            # Отправляем
            email.send()
            
            print("Email отправлен успешно!")
            
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
        
        return Response(
            {
                "message": "Резюме успешно отправлено", 
                "id": vacancy.id
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {"errors": form.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def download_resume(request, vacancy_id):
    try:
        vacancy = VacancyForm.objects.get(id=vacancy_id)
        if vacancy.resume and os.path.exists(vacancy.resume.path):
            with open(vacancy.resume.path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{vacancy.resume.name}"'
                return response
        return HttpResponse("Файл не найден", status=404)
    except VacancyForm.DoesNotExist:
        return HttpResponse("Резюме не найдено", status=404)
