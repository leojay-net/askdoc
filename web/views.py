from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .chat import get_response
from .serializers import ChatSerializer
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

class Chat(GenericAPIView):
    serializer_class = ChatSerializer
#     @extend_schema(
#     responses={
#       200: OpenApiResponse(
#         description="A Chat object with additional response field",
#         response=ChatSerializer,
#         examples=[
#           {
#             "problem": "ulcer",
#             "symptoms": "vommiting",
#             "medical_history": "stomach ache",
#             "response": "you need to see a medical doctor"
            
#           },
#           {
#             "problem": "head-ache",
#             "symptoms": "unable to sleep",
#             "medical_history": "body pains",
#             "response": "you need to see a medical doctor"
#           }
#         ],
#         request_only=False
#       )
#     }
#   )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            result = get_response(problem=serializer.data['problem'], symptoms=serializer.data['symptoms'], medical_history=serializer.data['medical_history'])
            response = serializer.data
            response["response"] = str(result)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)