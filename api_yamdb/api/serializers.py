from django.db.models import Avg
from rest_framework import serializers
from django.core.exceptions import ValidationError
import datetime

from reviews.models import Category,Genre,Title

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