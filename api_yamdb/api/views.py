from rest_framework import viewsets

from reviews.models import Titles, Categories, Genres

from api.serializers import (
    TitlesSerializer,
    CategoriesSerializer,
    GenresSerializer,
)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
