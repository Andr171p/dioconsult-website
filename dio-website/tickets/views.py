from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Ticket


@login_required
def ticket_list(request: HttpRequest) -> HttpResponse:
    """Просмтор списка тикетов в зависимости от роли пользователя"""

    user, profile = request.user, request.profile
    tickets = Ticket.objects.filter(created_by=user)
    if profile.role in ["support_agent", "support_manager"]:
        tickets = Ticket.objects.all()
    elif profile.role == "company_admin" and user.has_perm("tickets.view_company_tickets"):
        user_companies = user.companies.all()
        tickets = Ticket.objects.filter(company__in=user_companies)
    context = {"tickets": tickets}
    return render(request, "tickets/ticket_list.html", context)
