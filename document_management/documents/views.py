from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Document
from .serializers import DocumentSerializer
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Document.objects.all()

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def get_s3_client(self):
        """Create and return an S3 client using boto3."""
        return boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

    def perform_create(self, serializer):
        document = serializer.save(user=self.request.user)
        
        file_path = document.file.name

        try:
            s3_client = self.get_s3_client()
            s3_client.upload_file(
                Filename=document.file.path,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path
            )
            print(f"File uploaded to S3: {file_path}")

        except NoCredentialsError:
            print("Credentials not available")
        except Exception as e:
            print(f"An error occurred: {e}")

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        if document.user != request.user:
            raise PermissionDenied("You do not have permission to delete this document.")

        try:
            s3_client = self.get_s3_client()
            s3_client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=document.file.name
            )
            print(f"File deleted from S3: {document.file.name}")

        except NoCredentialsError:
            print("Credentials not available")
        except Exception as e:
            print(f"An error occurred: {e}")

        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        document = self.get_object()
        if document.user != request.user:
            raise PermissionDenied("You do not have permission to view this document.")
        return super().retrieve(request, *args, **kwargs)
