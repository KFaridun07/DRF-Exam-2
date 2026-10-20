from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Group,GroupMessage,GroupMember
from .serializers import GroupSerializer,GroupMemberSerializer,GroupMemberRoleSerializer,GroupMessageSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound

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

        if getattr(self, 'swagger_fake_view', False):

            return Group.objects.none()
        
        return Group.objects.filter(members__user=self.request.user,members__role__in=['owner', 'admin']).distinct()



class GroupDelete(generics.DestroyAPIView):
    queryset = Group.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Group.objects.none()
        return Group.objects.filter(owner=self.request.user)


class GroupMemberCreate(generics.CreateAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_group(self):
        return Group.objects.filter(
            id=self.kwargs['group_id'],
            members__user=self.request.user,
            members__role__in=['owner', 'admin']
        ).first()

    def perform_create(self, serializer):
        group = self.get_group()

        if group is None:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Vi ne mojete dobavlyat uchastnikov v etu gruppu')

        user = serializer.validated_data['user']

        if GroupMember.objects.filter(group=group, user=user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Etot polzovatel uje sostoit v gruppe')

        serializer.save(group=group, role='member')




class GroupMemberListView(generics.ListAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']

        if not GroupMember.objects.filter(group_id=group_id,user=self.request.user).exists():
  
            raise PermissionDenied('Вы не состоите в этой группе')

        return GroupMember.objects.filter(group_id=group_id)


class GroupMemberUpdateView(generics.UpdateAPIView):
    serializer_class = GroupMemberRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch', 'head', 'options']

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Group.objects.none()
        
        return GroupMember.objects.filter(group__owner=self.request.user)


class GroupMemberDeleteView(generics.DestroyAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Group.objects.none()

        return GroupMember.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.role == 'owner':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Vladelets ne mojet viyti iz gruppi')

        instance.delete()

class GroupMessageCreateView(generics.CreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GroupMessage.objects.all()

    def perform_create(self, serializer):
        group_id = self.kwargs['group_id']

        if not GroupMember.objects.filter(group_id=group_id,user=self.request.user).exists():
            raise PermissionDenied('Vi ne sostoite v etoy gruppe')

        group = Group.objects.filter(id=group_id).first()

        if group is None:
            raise NotFound('Group not found')

        serializer.save(user=self.request.user, group=group)


class GroupMessageListView(generics.ListAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']

        if not GroupMember.objects.filter(group_id=group_id,user=self.request.user).exists():
            raise PermissionDenied('Vi ne sostoite v etoy gruppe')

        return GroupMessage.objects.filter(group_id=group_id).order_by('cr_at')


class GroupMessageDeleteView(generics.DestroyAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GroupMessage.objects.filter(user=self.request.user)










    








