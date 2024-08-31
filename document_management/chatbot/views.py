from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ChatMessageSerializer
from .services import query_openai, generate_prompt, fetch_document_content


class ChatBotView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data["message"]
            document_id = serializer.validated_data["document_id"]

            document_content = fetch_document_content(request.user, document_id)

            if not document_content:
                return Response(
                    {"answer": "Document not found or inaccessible."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            prompt = generate_prompt(document_content, message)
            answer = query_openai(prompt)

            return Response({"answer": answer}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
