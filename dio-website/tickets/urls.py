from django.urls import path

from .views import InvitationActivateView

urlpatterns = [
    path(
        "invitation/<uuid:token>/", InvitationActivateView.as_view(), name="invitation_activate"
    )
]
