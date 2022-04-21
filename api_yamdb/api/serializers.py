import datetime

from django.core.exceptions import ValidationError
from django.forms import IntegerField
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Title, Comment, Review, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий, модели Category."""

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров, модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений, модели Title."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.rating

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

    def validate_year(self, data):
        if data > datetime.datetime.now().year:
            raise ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли',
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов, модели Review. """
    author = SlugRelatedField(slug_field='username', read_only=True)
    score = IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        if self.context["action"] != "create":
            return data
        if Review.objects.filter(
            title_id=self.context['title_id'], author=self.context['user']
        ).exists():
            raise serializers.ValidationError(
                'У вас уже есть отзыв на данное произведение.')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review
        read_only_fields = ['author']


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев, модели Comment. """

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['author']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей, модели User. """

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
    """Сериализатор для получения токена. """
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
