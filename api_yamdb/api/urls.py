from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TitlesViewSet, CategoriesViewSet, GenresViewSet

router_v1 = DefaultRouter()

router_v1.register('titles', TitlesViewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
