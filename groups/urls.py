from django.urls import path
from .views import *

urlpatterns = [
    path('groups/',GroupListCreateView.as_view()),
    path('<int:pk>/group/   ', GroupDetail.as_view()),
    path('<int:pk>/delete/', GroupDelete.as_view()),

]