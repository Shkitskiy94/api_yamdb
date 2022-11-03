from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import UsernameRegexValidator, username_me


class UserManager(BaseUserManager):
    """Переопределение базового менеджера user"""

    def create_user(self, email, username, **extra_fields):
        if not email:
            raise ValueError('Введите ваш email')
        if not username:
            raise ValueError('Введите ваше имя пользователя')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Введите ваш email')
        if not username:
            raise ValueError('Введите ваше имя пользователя')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


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
    confirmation_code = models.UUIDField(
        verbose_name='Confirmation code',
        default=0,
        editable=False,
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
