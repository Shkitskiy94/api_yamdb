import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Review, Title, Category, Genre
from users.models import User

from .permissions import (IsAdminModeratorOwnerOrReadOnly, IsAdmin)
from .serializers import (ReviewSerializer, CommentSerializer,
                          SendCodeSerializer, LogInSerializer,
                          AdminUserSerializer, UserSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleSerializerForView, TitleSerializerForWrite)

from .permissions import (IsAdminOrReadOnly)
from .mixins import CreateListDeleteViewSet
from .filters import TitleFilter


@api_view(['POST'])
def send_code(request):
    """View для отправки кода зарегистрированному пользователю"""
    serializer = SendCodeSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    confirmation_code = str(uuid.uuid4())
    if serializer.is_valid():

        if User.objects.filter(email=email, username=username).exists():
            user = User.objects.get(email=email, username=username)
            user.confirmation_code = confirmation_code
        else:
            User.objects.create_user(email=email, username=username)
        mail_subject = 'API_Yamdb: Ваш код аутентификации'
        mail_message = f'Скопируйте код: {confirmation_code}'
        send_mail(mail_subject, mail_message, 'API_Yamdb <admin@yamdb.ru>',
                  (email,), fail_silently=True)
        return Response(
            request.data,
            status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    """View для получения токена аутентификации"""
    serializer = LogInSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if confirmation_code == str(user.confirmation_code):
            token = RefreshToken.for_user(user)
            return Response({f'Your token: {token.access_token}'},
                            status=status.HTTP_200_OK)
        return Response('Wrong code',
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(viewsets.ModelViewSet):
    """ViewSet для admins"""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    filter_fields = ('role',)
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


class UserInfo(APIView):
    """View для получения информации о пользователе"""
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response('You are not authenticated',
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response('Вы не авторизованы',
                        status=status.HTTP_401_UNAUTHORIZED)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDeleteViewSet):
    """Класс представления категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDeleteViewSet):
    """Класс представления жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Класс представления произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializerForView
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleSerializerForWrite
        return TitleSerializerForView
