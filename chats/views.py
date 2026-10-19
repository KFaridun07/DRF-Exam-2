from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from .serializers import ChatSerializer
from .models import Chat
from django.db import models
from django.db.models import Q

# Create your views here.

class CreateChat(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_1 = self.request.user
        user_2 = serializer.validated_data['user_2']

        if user_1 == user_2:
            raise ValidationError('Chat s samim soboy ne vozmojno')
        chat_exists = Chat.objects.filter(user_1=user_1,user_2 = user_2).exists() or Chat.objects.filter(user_1 = user_2,user_2 = user_1).exists()
        if chat_exists:
            raise ValidationError('Chat s etim polzovatelem sushestvuet')
        serializer.save(user_1 = user_1)

class ChatList(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Chat.objects.filter(Q(user_1 = user) | Q(user_2 = user)).order_by('-cr_at')


class ChatDetail(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Chat.objects.none()

        user = self.request.user

        return Chat.objects.filter(models.Q(user_1=user) | models.Q(user_2=user))




class ChatDelete(generics.DestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Chat.objects.none()

        user = self.request.user

        return Chat.objects.filter(models.Q(user_1=user) | models.Q(user_2=user))




