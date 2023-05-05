from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import AdminOrReadOnly


class CreateListViewSet(mixins.DestroyModelMixin,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet,):
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
