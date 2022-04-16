from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import User


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
        fields = ("email", "username")

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
