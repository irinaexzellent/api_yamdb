from rest_framework import generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
import django_filters


from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .pagination import CategoryGenrePagination


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def get_permissions(self):
        # if self.action == 'create':
        # return (AdminostratorOnly(),)
        return super().get_permissions()


class CategoryDelete(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    #permission_classes = (AdminOnly,)


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def get_permissions(self):
        # if self.action == 'create':
        # return (AdminostratorOnly(),)
        return super().get_permissions()


class GenreDelete(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    #permission_classes = (AdminOnly,)


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


class TitleList(generics.ListCreateAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class TitleViewSet(generics.RetrieveDestroyAPIView):
    serializer_class = TitleSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('pk')
        return Title.objects.filter(pk=title_id)
