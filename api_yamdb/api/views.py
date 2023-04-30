import secrets
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.generics import CreateAPIView
from reviews.models import Categories, Comments, Genres, Reviews, Titles
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitlesSerializer,
    TokenObtainPairSerializer,
    UserSerializer,
    UserSignUpSerializer,
)
from rest_framework.response import Response # for UserSignUpView
from api_yamdb import settings # for UserSignUpView
from django.core.mail import send_mail # for UserSignUpView
from rest_framework import status # for UserSignUpView
from .permissions import IsAuthorOrReadOnly, AdminAndSuperUser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from rest_framework import status, viewsets



class TokenObtainPairView(TokenViewBase): #in url
    serializer_class = TokenObtainPairSerializer


class UserSignUpView(CreateAPIView): #in url
    serializer_class = UserSignUpSerializer
    # permission_classes = (AdminAndSuperUser,)

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

class UserViewSet(viewsets.ModelViewSet): # in url
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class TitlesViewSet(viewsets.ModelViewSet): # in url
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class CategoriesViewSet(viewsets.ModelViewSet): # in url
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet): # in url
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class ReviewsViewSet(viewsets.ModelViewSet): # in url
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id'))
        return Reviews.objects.filter(title=title)
    
    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))
        if title.reviews.filter(author=self.request.user).exists():
            raise ValidationError("Можно добавить только один отзыв к произведению")
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrReadOnly]
