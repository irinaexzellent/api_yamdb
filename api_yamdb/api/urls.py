from api.views import CommentsViewSet, ReviewsViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APISignUp, APIToken, CategoryDelete, CategoryListCreate,
                    GenreDelete, GenreListCreate, TitleList, TitleViewSet,
                    UsersViewSet)

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
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/categories/', CategoryListCreate.as_view()),
    path('v1/categories/<slug>/', CategoryDelete.as_view()),
    path('v1/genres/', GenreListCreate.as_view()),
    path('v1/genres/<slug>/', GenreDelete.as_view()),
    path('v1/titles/', TitleList.as_view()),
    path('v1/titles/<pk>/', TitleViewSet.as_view()),
    path('v1/auth/token/', APIToken.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/signup/', APISignUp.as_view()),
]
