import datetime

from django.core.exceptions import ValidationError
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, Comments, Review, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий, модели Category."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров, модели Genre."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений, модели Title."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    description = required = False
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def validate(self, data):
        """Валидатор проверяет год произведения."""

        if data['year'] > datetime.datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение, которое еще не вышло.')
        return data

    def get_rating(self, obj):
        """Расчет среднего показателя рейтинга из всех оценок."""

        rating = obj.Titles_review.aggregate(Avg('score')).get('score__avg')
        return rating


class PostTitleSerializer(serializers.ModelSerializer):
    """Сериализатор метода POST, модели Title. """

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review
        read_only_fields = ['author']


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев, модели Comment. """

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ['author']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',
                  )


class AuthSerializer(serializers.ModelSerializer):
    """Сериализатор для аутентификации пользователя. """

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, data):

        if data == 'me':
            raise ValidationError(
                message='Нельзя создать пользователя с username = me!')
        return data


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class RoleforReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
