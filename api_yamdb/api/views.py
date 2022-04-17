# from django.shortcuts import get_object_or_404 #раскоментить после merge#
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from reviews.models import Category, Comments, Genre, Review, Title

from .pagination import CategoryGenrePagination
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
#        get_object_or_404(Titles, id=title_id)   #раскоментить после merge#
        new_queryset = Review.objects.filter(title_id=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
#        get_object_or_404(Titles, id=title_id)    #раскоментить после merge#
        serializer.save(author=self.request.user,
                        title_id=title_id)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
#        get_object_or_404(Review, id=review_id)   #раскоментить после merge#
        new_queryset = Comments.objects.filter(review_id=review_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("review_id")
#        get_object_or_404(Review, id=review_id)    #раскоментить после merge#
        serializer.save(author=self.request.user,
                        title_id=title_id)


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
