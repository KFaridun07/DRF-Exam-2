from django.urls import path,re_path
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login/', PhoneTokenView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('me/', MeView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profiles/',ProfileListCreateView.as_view()),
    path('profile/<int:pk>',ProfileDetail.as_view()),
    path('profiles/me',MyProfileUpdate.as_view()),
    path('avatars/',AvatarCreate.as_view()),
    path('avatars/my/', MyAvatarList.as_view()),
    path('avatars/<int:pk>/delete/',MyAvatarDelete.as_view()),



    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
