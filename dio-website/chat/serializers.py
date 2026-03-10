from typing import ClassVar

from rest_framework import serializers


class ChatMessageSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)

    class Meta:
        fields: ClassVar[list] = ["content"]


class AddDocumentSerializer(serializers.Serializer):
    text = serializers.DictField(required=True)

    class Meta:
        fields: ClassVar[list] = ["text"]


class DeleteDocumentSerializer(serializers.Serializer):
    ids = serializers.ListField(required=True)

    class Meta:
        fields: ClassVar[list] = ["ids"]
