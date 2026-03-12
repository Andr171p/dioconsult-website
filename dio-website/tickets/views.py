from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import SetPasswordForm
from .models import CounterpartyUser, Invitation, Profile, Ticket

User = get_user_model()


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


class InvitationActivateView(FormView):
    template_name = "invitation_activate.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("tickets:dashboard")
    invitation: Invitation | None = None

    def dispatch(
            self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponseBase:
        self.invitation = get_object_or_404(Invitation, token=kwargs["token"])
        if not self.invitation.is_valid():
            messages.error(request, "Ссылка устарела или уже использована.")
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        user = User.objects.create_user(
            username=self.invitation.email,
            email=self.invitation.email,
            password=form.cleaned_data["password"]
        )
        if not self.invitation.counterparty.counterpartyuser_set.exists():
            role = "admin"
            can_view_all = True
        else:
            role = self.invitation.default_counterparty_role
            can_view_all = (role == "admin")
        Profile.objects.create(
            user=user, role="counterparty_user", email_notifications_enables=True
        )
        CounterpartyUser.objects.create(
        user=user,
            counterparty=self.invitation.counterparty,
            role=role,
            can_create_tickets=True,
            can_view_all_tickets=can_view_all
        )
        self.invitation.mark_as_used()
        self.invitation.counterparty.users.add(user)
        self.invitation.save()
        login(self.request, user)
        messages.success(self.request, "Учётная запись успешно создана. Добро пожаловать!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["counterparty_name"] = self.invitation.counterparty.name
        ctx["email"] = self.invitation.email
        return ctx
