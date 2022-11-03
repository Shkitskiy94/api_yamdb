from django.db import models
from .validators import year_validator

class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(
        'Категория',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        'Cлаг',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        'Жанр',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Произведения, к которым пишут отзывы."""
    name = models.CharField(
        'Название произведения',
        max_length=200
    )
    year = models.IntegerField('Дата выпуска',validators=[year_validator])
    descriptions = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        blank=True,
        related_name = 'titles',
        verbose_name = 'Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category',
        verbose_name = 'Категория'
    )
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
    
    def __str__(self):
        return self.name

