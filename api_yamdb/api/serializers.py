from rest_framework import serializers

from users.models import User


class SendCodeSerializer(serializers.Serializer):
    """Serializer для отправки кода по электронной почте"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Некорректное имя пользователя')
        return value

    def validate(self, attrs):
        username_exists = User.objects.filter(
            username=attrs['username']).exists()
        email_exists = User.objects.filter(
            email=attrs['email']).exists()
        if username_exists and not email_exists:
            raise serializers.ValidationError('Пользователь уже существует')
        if email_exists and not username_exists:
            raise serializers.ValidationError('Пользователь уже существует')
        return attrs


class LogInSerializer(serializers.Serializer):
    """Serializer для входа"""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer для admin"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')


class UserSerializer(serializers.ModelSerializer):
    """Serializer для простых пользователей"""
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'bio',
                  'first_name',
                  'last_name',
                  'role'
                  )
        read_only_fields = ('role',)
