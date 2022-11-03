from django.db.models import Avg
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import Title, Review, Comment, Category, Genre
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


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзывов и оценок"""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 5:
            raise serializers.ValidationError('Оценка по 5-бальной шкале')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Доступен только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для комментариев"""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializerForWrite(serializers.ModelSerializer):
    """Сериализатора для добавления,изменения,удаления произведений."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    class Meta:
        fields = '__all__'
        model = Title
    
    def year_validator(value):
        """Валидация даты."""
        if value < 1900 or value > datetime.datetime.now().year:
            raise ValidationError(
                ('%(value)s is not a correct year!'),
                params={'value': value},
            )

class TitleSerializerForView(serializers.ModelSerializer):
    """Сериализатора для обзора произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title
        read_only_fields = ('id', 'rating')
    
    def get_avg_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))
        return rating
