# vacancy/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('vacancy-unprocessed-count/', views.vacancy_unprocessed_count),
    path('latest-unprocessed-vacancy/', views.latest_unprocessed_vacancy),
]
