from rest_framework import serializers

class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    document_id = serializers.IntegerField()
