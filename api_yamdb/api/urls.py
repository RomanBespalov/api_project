from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoriesViewSet,
    CommentsViewSet,
    GenresViewSet,
    ReviewsViewSet,
    TitlesViewSet
)

router_v1 = DefaultRouter()

router_v1.register('titles', TitlesViewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
