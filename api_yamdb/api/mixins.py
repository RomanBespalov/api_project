from rest_framework import mixins, viewsets

from api.permissions import AdminOrReadOnly


class CreateListViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    AdminOrReadOnly
):
    pass
