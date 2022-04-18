from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    CommentsViewSet,
    ReviewsViewSet
)
from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register(
    'genres',
    GenreViewSet, basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet, basename='categores'
)
router_v1.register(
    'titles',
    TitleViewSet, basename='titles'
)
router_v1.register(
    r'titles/(?P<title_id>\w+)/review',
    ReviewsViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\w+)/review/(?P<review_id>\w+)/comments',
    CommentsViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
