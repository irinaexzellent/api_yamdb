# from django.shortcuts import get_object_or_404 #раскоментить после merge#
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comments, Review
from .serializers import CommentsSerializer, ReviewSerializer


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
