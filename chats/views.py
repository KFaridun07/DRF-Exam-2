from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from .serializers import ChatSerializer
from .models import Chat

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
        

