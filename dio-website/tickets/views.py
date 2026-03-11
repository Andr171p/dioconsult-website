from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import SetPasswordForm
from .models import Invitation, Profile, Ticket

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
    success_url = reverse_lazy("login")
    invitation: Invitation | None = None

    def dispatch(
            self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponseBase:
        self.invitation = get_object_or_404(Invitation, token=kwargs["token"])
        if not self.invitation.is_valid():
            messages.error(request, "Ссылка устарела или уже была использована.")
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        user = User.objects.create_user(
            username=self.invitation.email,
            email=self.invitation.email,
            password=form.cleaned_data["password"]
        )
        Profile.objects.create(user=user, role="company_user")
        self.invitation.company.users.add(user)
        self.invitation.mark_as_used()
        self.invitation.save()
        messages.success(...)
        return super().form_valid(form)
