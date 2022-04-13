from django.shortcuts import render

from rest_framework import viewsets

from reviews.models import Category
from .serializers import CategorySerializer
from .pagination import CategoryPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
