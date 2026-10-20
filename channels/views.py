from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Channel
from .serializers import ChannelSerializer
from django.db.models import Q







class ChannelCreateView(generics.CreateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,link=f"channel-{self.request.user.id}-{Channel.objects.count() + 1}")


class ChannelListView(generics.ListAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Channel.objects.filter(type='public')


class ChannelDetailView(generics.RetrieveAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Channel.objects.filter(Q(type='public') |Q(owner=self.request.user) |Q(followers__user=self.request.user)).distinct()


class ChannelUpdateView(generics.UpdateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Channel.objects.filter(owner=self.request.user)


class ChannelDeleteView(generics.DestroyAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Channel.objects.filter(owner=self.request.user)