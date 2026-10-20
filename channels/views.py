from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Channel,ChannelFollow
from .serializers import ChannelSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView







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


class ChannelFollowView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        channel_id = self.kwargs['channel_id']

        channel = Channel.objects.filter(id=channel_id).first()

        if not channel:
            return Response(
                {'error': 'Channel not found'},status=404)

        if channel.type == 'private' and channel.owner != request.user:
            return Response({'error': 'Nelzya podpostsya na privatniy channel'},status=403)

        if ChannelFollow.objects.filter(user=request.user,channel=channel).exists():
            return Response({'error': 'Vi podpisani na kanal'},status=400)

        ChannelFollow.objects.create(user=request.user,channel=channel)

        return Response({'message': 'Vi podpisalis na kanal'},status=201)


class ChannelUnfollowView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChannelFollow.objects.filter(user=self.request.user,channel_id=self.kwargs['channel_id'])


class FollowingListView(generics.ListAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Channel.objects.filter(followers__user=self.request.user)


class IsFollowingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, channel_id):
        is_following = ChannelFollow.objects.filter(user=request.user,channel_id=channel_id).exists()

        return Response({'channel_id': channel_id,'is_following': is_following})

