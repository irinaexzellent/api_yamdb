import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters, viewsets

from reviews.models import Category, Genre, Title
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    PostTitleSerializer,
)
from .pagination import CategoryGenrePagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        # if self.action in ['create', 'destroy']:
        # return (IsAdminOnly(),)
        return super().get_permissions()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        # if self.action in ['create', 'destroy']:
        # return (IsAdminOnly(),)
        return super().get_permissions()


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name')
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('reviews__score'),)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return PostTitleSerializer

    def get_permissions(self):
        # if self.action in ['create', 'destroy', 'partial_update']:
        # return (IsAdminOnly(),)
        return super().get_permissions()

    # def get_queryset(self):
        # return Title.objects.all().annotate(rating=Avg('reviews__score'),)
