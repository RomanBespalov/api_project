from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (TitlesViewSet,
                       CategoriesViewSet,
                       GenresViewSet,
                       TokenObtainPairView,
                       UserSignUpView,
                       UserViewSet,
                       ReviewsViewSet,
                       CommentsViewSet,)


router_v1 = DefaultRouter()

router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comment')
auth_urls = [
    path(
        'auth/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/signup/', UserSignUpView.as_view(),
        name='sign_up'
    ),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(auth_urls)),
]
