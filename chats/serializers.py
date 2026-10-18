from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Chat


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id','user_1','user_2','cr_at']
        read_only_fields = ['id','user_1','user_2']
        