from django.urls import path
from .views import *


urlpatterns = [
    path('chats/', ChatList.as_view()),
    path('create/', CreateChat.as_view()),
    path('<int:pk>/', ChatDetail.as_view()),
    path('<int:pk>/delete/', ChatDelete.as_view()),
]