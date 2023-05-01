from django.contrib.auth import get_user_model
from .registration.token_generator import get_tokens_for_user
from reviews.models import Categories, Comments, Genres, Reviews, Titles
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from api.permissions import IsAuthorOrReadOnly, AdminOrReadOnly
from api.serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitlesSerializer,
    UserSerializer,
    CreateTitlesSerializer,
    SignUpSerializer,
    GetTokenSerializer,
    UserProfileSerializer,
)
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly, AdminAndSuperUser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db.models import Avg
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from reviews.models import User
from .registration.send_code_to_email import send_confirm_code_to_email
from .registration.token_generator import get_tokens_for_user
from .registration.confirm_code_generator import generator
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet)
from rest_framework.permissions import IsAuthenticated


class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminAndSuperUser,)
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = "username"
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            if User.objects.filter(email=email).first():
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            user, created = User.objects.get_or_create(**serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data['username']
        email = serializer.data['email']

        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        user.confirmation_code = generator()
        user.save()
        send_confirm_code_to_email(user, email)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data['username']
        code = serializer.data['confirmation_code']
        if User.objects.filter(username=username).first():
            user = User.objects.get(username=username)
            if user.confirmation_code == code:
                token = get_tokens_for_user(user)
                return Response(token, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Titles
        fields = ('name', 'year')


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(rating=Avg("reviews__score"))
    permission_classes = (AdminOrReadOnly,)
    serializer_class = TitlesSerializer
    create_serializer_class = CreateTitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return self.create_serializer_class
        return self.serializer_class


    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return self.create_serializer_class
        return self.serializer_class


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
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


@api_view(['PATCH', 'GET'])
@permission_classes([IsAuthenticated])
def me(request):
    if request.method == "GET":
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        serializer = UserProfileSerializer(
            request.user, partial=True, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
