from rest_framework import serializers
from .models import Group,GroupMember,GroupMessage
from rest_framework.serializers import ModelSerializer

class GroupSerializer(ModelSerializer):
    class Meta:
        model  = Group
        fields = ['id', 'title', 'avatar']
        read_only_fields = ['id']


