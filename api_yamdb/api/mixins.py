from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins, viewsets, filters

from api.permissions import AdminOrReadOnly


class CreateListViewSet(mixins.DestroyModelMixin,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet,):
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
