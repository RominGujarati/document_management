import openai
import boto3
from django.conf import settings
from documents.models import Document
from rest_framework.response import Response
import os

openai.api_key = settings.OPENAI_API_KEY


def chunk_text(text, max_chunk_size):
    """Splits the text into chunks of specified maximum size."""
    chunks = []
    while len(text) > max_chunk_size:
        chunk = text[:max_chunk_size]
        chunks.append(chunk)
        text = text[max_chunk_size:]
    chunks.append(text)
    return chunks


def query_openai(prompt):
    """Query OpenAI API with a given prompt."""
    chunks = chunk_text(prompt, max_chunk_size=3000)
    responses = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            engine="gpt-3.5-turbo", prompt=prompt, max_tokens=150
        )
        answer = response.choices[0].text.strip()
        responses.append(answer)
    return Response({"answer": " ".join(responses)})


def generate_prompt(document_content, question):
    """Generate a prompt to send to OpenAI API."""
    return f"Based on the following document, answer the question:\n\nDocument:\n{document_content}\n\nQuestion: {question}\n\nAnswer:"


def get_s3_client():
    """Create and return an S3 client using boto3."""
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )


def fetch_document_from_s3(user, document_id):
    """Fetch a specific document content from S3 based on the document ID."""
    s3_client = get_s3_client()
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    try:
        document = Document.objects.get(id=document_id, user=user)
        response = s3_client.get_object(Bucket=bucket_name, Key=document.file.name)
        return response["Body"].read().decode("utf-8")
    except Document.DoesNotExist:
        return None
    except Exception as e:
        print(f"An error occurred while fetching the document from S3: {e}")
        return None


def fetch_document_from_local(document_id):
    """Fetch a specific document content from local storage based on the document ID."""
    try:
        document = Document.objects.get(id=document_id)
        file_name = os.path.basename(document.file.name)
        file_path = os.path.join(settings.LOCAL_DOCUMENTS_DIR, file_name)

        print(f"Attempting to fetch local file from: {file_path}")

        if not os.path.exists(file_path):
            print(f"Local file does not exist: {file_path}")
            return None

        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext in [".txt", ".csv", ".json", ".xml"]:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            with open(file_path, "rb") as file:
                return file.read()
    except Document.DoesNotExist:
        return None
    except Exception as e:
        print(f"An error occurred while fetching the document from local storage: {e}")
        return None


def fetch_document_content(user, document_id):
    """Fetch document content from S3 or fallback to local storage."""
    document_content = fetch_document_from_s3(user, document_id)
    if not document_content:
        document_content = fetch_document_from_local(document_id)
    return document_content
