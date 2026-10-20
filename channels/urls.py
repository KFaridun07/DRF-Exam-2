from django.urls import path
from .views import *



urlpatterns = [
    path('channels/', ChannelCreateView.as_view()),
    path('channels/list/', ChannelListView.as_view()),
    path('channels/<int:pk>/', ChannelDetailView.as_view()),
    path('channels/<int:pk>/edit/', ChannelUpdateView.as_view()),
    path('channels/<int:pk>/delete/', ChannelDeleteView.as_view()),

    
]
