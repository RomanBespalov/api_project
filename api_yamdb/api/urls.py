from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (TitlesViewSet,
                       CategoriesViewSet,
                       GenresViewSet,
                       UserViewSet,
                       ReviewsViewSet,
                       CommentsViewSet,)
from . import views

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='review')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comment')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/', include(router_v1.urls)),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.signup),
    path('v1/auth/token/', views.get_token),
]



# urlpatterns = [
#     path('v1/auth/signup/', views.signup),
#     path('v1/auth/token/', views.get_token),
#     path('v1/users/me/', views.me),
#     path('', include(router_v1.urls)),
# ]
# path('api/', include('users.urls')),