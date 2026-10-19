from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Group,GroupMessage,GroupMember
from .serializers import GroupSerializer

# Create your views here.


class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(members__user=self.request.user).distinct()

    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)

        GroupMember.objects.create(user=self.request.user,group=group,role='owner')



class GroupDetail(generics.RetrieveUpdateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        return Group.objects.filter(members__user=self.request.user,members__role__in=['owner', 'admin']).distinct()



class GroupDelete(generics.DestroyAPIView):
    queryset = Group.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(owner=self.request.user)

    

    



    








