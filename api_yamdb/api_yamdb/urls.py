from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #Авторизация по JWT-токенам
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #Авторизация по JWT-токенам
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'), #Авторизация по JWT-токенам
    
]
