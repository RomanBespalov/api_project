from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .registration.send_code_to_email import send_confirm_code_to_email
from .registration.token_generator import get_tokens_for_user
from .registration.confirm_code_generator import generator
from api.filters import TitleFilter
from api.permissions import AdminOrReadOnly
from api.paginators import CustomPagination
from api.permissions import (AdminAndSuperUser,
                             AuthorAdminModeratorOrReadOnly)
from reviews.models import Category, Comment, Genre, Review, Title, User
from api.serializers import (CategoriesSerializer,
                             CommentsSerializer,
                             GenresSerializer,
                             ReviewsSerializer,
                             TitlesSerializer,
                             UserSerializer,
                             CreateTitlesSerializer,
                             SignUpSerializer,
                             GetTokenSerializer,)
from api.mixins import CreateListViewSet


'''Пользовательские представления.'''


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
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        if User.objects.filter(email=email).first():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        _, _ = User.objects.get_or_create(**serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=("get", "patch"),
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == "GET":
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.validated_data["role"] = request.user.role
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user, _ = User.objects.get_or_create(
        username=username,
        email=email
    )
    user.confirmation_code = generator()
    user.save()
    send_confirm_code_to_email(user, email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data['username']
        code = serializer.data['confirmation_code']
        if user := User.objects.filter(username=username).first():
            if user.confirmation_code == code:
                token = get_tokens_for_user(user)
                return Response(token, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''Титлы, Комменты, Жанры, Категории, Ревью'''


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
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


class CategoriesViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [AuthorAdminModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"),
        )
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"),
        )
        serializer.save(author=self.request.user, review=review)
