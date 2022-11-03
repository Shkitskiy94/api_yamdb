from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
    pass

class Title(models.Model):
    pass


class Review(models.Model):
    """Отзывы на произведения.
    Отзыв привязан к определённому произведению (class Title)"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.CharField(
        'Текст отзыва',
        max_length=200
    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(5)
        ),
        error_messages={'validators': 'Оценка от 1 до 5'}
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        
    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к отзывам.
    Комментарий привязан к определённому отзыву (class Review)"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.CharField(
        'Текст комментария',
        max_length=200
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
