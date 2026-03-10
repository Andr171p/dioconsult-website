from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .forms import FeedbackForm


@api_view(["POST"])
@parser_classes([JSONParser])
def feedback_view(request) -> Response:
    form = FeedbackForm(request.data)
    if form.is_valid():
        form.save()
        return Response(status=status.HTTP_200_OK)
    return Response(
        status=status.HTTP_400_BAD_REQUEST,
    )
