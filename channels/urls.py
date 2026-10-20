from django.urls import path
from .views import *



urlpatterns = [
    path('channels/', ChannelCreateView.as_view()),
    path('channels/list/', ChannelListView.as_view()),
    path('channels/<int:pk>/', ChannelDetailView.as_view()),
    path('channels/<int:pk>/edit/', ChannelUpdateView.as_view()),
    path('channels/<int:pk>/delete/', ChannelDeleteView.as_view()),
    path('channels/<int:channel_id>/follow/',ChannelFollowView.as_view()),
    path('channels/<int:channel_id>/unfollow/',ChannelUnfollowView.as_view()),
    path('channels/<int:channel_id>/list-following/',FollowingListView.as_view()),
    path('channels/<int:channel_id>/is-following/',IsFollowingView.as_view()),

    
]
