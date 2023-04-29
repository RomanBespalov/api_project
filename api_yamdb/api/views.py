import secrets
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.generics import CreateAPIView
from reviews.models import Titles, Categories, Genres
from .serializers import TokenObtainPairSerializer, UserSignUpSerializer
from api.serializers import (
    TitlesSerializer,
    CategoriesSerializer,
    GenresSerializer,
    UserSerializer,
)
from rest_framework.response import Response # fro UserSignUpView
from api_yamdb import settings # for UserSignUpView
from django.core.mail import send_mail # for UserSignUpView
from rest_framework import status # for UserSignUpView
from .permissions import IsAdminOrReadOnly



class TokenObtainPairView(TokenViewBase): 
    serializer_class = TokenObtainPairSerializer


class UserSignUpView(CreateAPIView): 
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = secrets.token_urlsafe()
        user, _ = get_user_model().objects.get_or_create(
            username=serializer.data.get('username'),
            email=serializer.data.get('email'),
            confirmation_code=token
        )
        message = (f'Для подтверждения регистрации на сайте '
                   f'пожалуйста, переходите по данной ссылке: {settings.HOST_NAME}?code={token}')
        send_mail(
            subject='Регистрация на сайте',
            message=message,
            from_email=settings.FROM_EMAIL,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminOrReadOnly,)
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminOrReadOnly,)
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminOrReadOnly,)
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
