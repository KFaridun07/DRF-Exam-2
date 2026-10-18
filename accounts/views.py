from django.shortcuts import render
from rest_framework import generics, permissions,status
from .serializers import UserSerializer,PhoneTokenSerializer,ProfileSerializer,AvatarSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Profile,Avatar
from django.db import models
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser





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

class ProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description='Поиск по имени, фамилии или username',
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.query_params.get('search', '')

        profiles = Profile.objects.all()

        if search:
            profiles = profiles.filter(
                Q(firstname__icontains=search) |
                Q(lastname__icontains=search) |
                Q(username__icontains=search)
            )

        return profiles

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyProfileUpdate(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user_id = self.request.user)


class ProfileSearchView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search = self.request.query_params.get('search')

        profiles = Profile.objects.all()

        if search:
            profiles = profiles.filter(
                models.Q(firstname__icontains=search) |
                models.Q(lastname__icontains=search) |
                models.Q(username__icontains=search)
            )

        return profiles

class AvatarCreate(generics.CreateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def perform_create(self, serializer):
        profile = Profile.objects.get(user_id=self.request.user)
        serializer.save(profile=profile)


class MyAvatarList(generics.ListAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user_id = self.request.user)
        return Avatar.objects.filter(profile = profile)


class MyAvatarDelete(generics.DestroyAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Avatar.objects.none()

        profile = Profile.objects.get(user_id=self.request.user)
        return Avatar.objects.filter(profile=profile)







