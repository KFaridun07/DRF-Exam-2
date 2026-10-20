from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'title', 'description', 'type', 'link', 'owner', 'cr_at']
        read_only_fields = ['id', 'link', 'owner', 'cr_at']