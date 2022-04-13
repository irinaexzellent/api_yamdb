from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comments, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comments
