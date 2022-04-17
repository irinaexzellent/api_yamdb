from django.urls import path


from .views import (
    CategoryListCreate,
    CategoryDelete,
    GenreListCreate,
    GenreDelete,
    TitleViewSet,
    TitleList,
)


urlpatterns = [
    path('v1/categories/', CategoryListCreate.as_view()),
    path('v1/categories/<slug>/', CategoryDelete.as_view()),
    path('v1/genres/', GenreListCreate.as_view()),
    path('v1/genres/<slug>/', GenreDelete.as_view()),
    path('v1/titles/', TitleList.as_view()),
    path('v1/titles/<pk>/', TitleViewSet.as_view()),
]
