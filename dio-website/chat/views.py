from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .rest import add_document, delete_document, get_ai_response, upload_document
from .serializers import AddDocumentSerializer, ChatMessageSerializer, DeleteDocumentSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat(request) -> Response:
    serializer = ChatMessageSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"error": "Invalid input", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    session_id = request.COOKIES.get("sessionid")
    content = serializer.validated_data["content"]
    payload = {"id": session_id, "role": "human", "content": content}

    api_response = get_ai_response(payload)

    return Response(api_response, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_document_(request) -> Response:
    serializer = AddDocumentSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"error": "Invalid input", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    text = serializer.validated_data["text"]
    return Response(add_document(text), status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_document_(request) -> Response:
    if "file" not in request.FILES:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    file_obj = request.FILES["file"]

    return Response(upload_document(file_obj), status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_document_(request) -> Response:
    serializer = DeleteDocumentSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"error": "Invalid input", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    ids = serializer.validated_data["ids"]
    return Response(delete_document(ids), status=status.HTTP_204_NO_CONTENT)
