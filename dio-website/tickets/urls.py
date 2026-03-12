from django.urls import path

from .views import InvitationActivateView

urlpatterns = [
    path(
        "invitation/activate/<uuid:token>/",
        InvitationActivateView.as_view(),
        name="invitation_activate"
    )
]
