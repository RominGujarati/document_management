from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    signed_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'file', 'created_at', 'signed_url']

    def get_signed_url(self, obj):
        return obj.get_signed_url()
