from django.urls import path

from api.views import ReviewsViewSet, CommentsViewSet

app_name = 'api'

urlpatterns = [
    path('v1/reviews/', ReviewsViewSet.as_view(
         {'get': 'list', 'post': 'create'}), name='review'),
    path('v1/comments/', CommentsViewSet.as_view(
         {'get': 'list', 'post': 'create'}), name='comment'),
]
