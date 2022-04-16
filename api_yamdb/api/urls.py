from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import APISignUp, APIToken, UsersViewSet


router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', APIToken.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/signup/', APISignUp.as_view()),
]
