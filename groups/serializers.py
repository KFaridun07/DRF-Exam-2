from rest_framework import serializers
from .models import Group,GroupMember,GroupMessage
from rest_framework.serializers import ModelSerializer

class GroupSerializer(ModelSerializer):
    class Meta:
        model  = Group
        fields = ['id', 'title', 'avatar']
        read_only_fields = ['id']



class GroupMemberSerializer(ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['id', 'user', 'group', 'role', 'joining_date']
        read_only_fields = ['id', 'group', 'role', 'joining_date']


class GroupMemberRoleSerializer(ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['role']

class GroupMessageSerializer(ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = ['id', 'user', 'group', 'content', 'cr_at']
        read_only_fields = ['id', 'user', 'group', 'cr_at']



