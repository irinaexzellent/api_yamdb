from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CommentsViewSet, ReviewsViewSet

app_name = 'api'

router = SimpleRouter()

router.register(
    r'titles/(?P<title_id>\w+)/review',
    ReviewsViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\w+)/review/(?P<review_id>\w+)/comments',
    CommentsViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
