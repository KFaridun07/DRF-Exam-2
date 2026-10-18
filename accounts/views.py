from django.shortcuts import render
from rest_framework import generics, permissions,status
from .serializers import UserSerializer,PhoneTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class PhoneTokenView(TokenObtainPairView):
    serializer_class = PhoneTokenSerializer


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"id": request.user.id,"phone": request.user.phone})



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh'],
        properties={
            'refresh': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Refresh token'
            )
        }
    )
)

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'},status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'detail': 'Logout successful.'},status=status.HTTP_205_RESET_CONTENT)
        except Exception:

            return Response({'detail': 'Invalid or expired refresh token.'},status=status.HTTP_400_BAD_REQUEST)


