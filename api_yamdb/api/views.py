from rest_framework import viewsets

from reviews.models import Category
from .serializers import CategorySerializer
from .pagination import CategoryPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    def destroy(self, request, pk=None):
        return super().destroy(request)
    
    def get_permissions(self):
#        if self.action == 'create' or 'destroy':
#            return (AdminostratorOnly(),)
        return super().get_permissions()