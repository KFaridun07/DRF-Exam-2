from django.urls import path
from .views import *

urlpatterns = [
    path('groups/',GroupListCreateView.as_view()),
    path('<int:pk>/group/   ', GroupDetail.as_view()),
    path('<int:pk>/delete/', GroupDelete.as_view()),
    path('<int:group_id>/members/', GroupMemberCreate.as_view()),
    path('<int:group_id>/memberslist/', GroupMemberListView.as_view()),
    path('<int:group_id>/members/<int:pk>/',GroupMemberUpdateView.as_view()),
    path('members/<int:pk>/delete/', GroupMemberDeleteView.as_view()),

]