from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import UsernameRegexValidator, username_me


class User(AbstractUser):
    """Модель пользователей, с валидацией имени пользователя"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES_ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )
    username_validator = UsernameRegexValidator()
    username = models.CharField(
        max_length=30,
        unique=True,
        help_text='Набор символов не более 30.'
                  'Только буквы, цифры и @/./+/-/_',
        validators=[username_validator, username_me],
        error_messages={
            'unique': "Пользователь с таким именем уже существует!",
        },
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=16,
        choices=CHOICES_ROLE,
        default='user',
        verbose_name='Роль',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
