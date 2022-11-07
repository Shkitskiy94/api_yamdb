from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from .filters import TitleFilter
from .mixins import AdminViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrModeRatOrOrAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          SignUpSerializer, TitlePostSerialzier,
                          TitleSerializer, TokenRegSerializer,
                          UserEditSerializer, UserSerializer)


from reviews.models import Category, Genre, Review, Title
from users.models import User


@api_view(['POST'])
def signup(request):
    """View для авторизации пользователей.
    Ограничения по пермишенам (для всех доступно)"""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError:
        return Response('Это имя или email уже занято',
                        status.HTTP_400_BAD_REQUEST)
    code = default_token_generator.make_token(user)
    send_mail(
        'Код токена',
        f'Код для получения токена {code}',
        settings.DEFAULT_FROM_EMAIL,
        [serializer.validated_data.get('email')]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class TokenRegApiView(APIView):
    """View для авторизации по токену"""
    def post(self, request):
        serializer = TokenRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            message = (
                'Вы использовали неправильный или чужой код подтверждения.')
            return Response({message}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)},
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """View для получения информации о пользователе"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'

    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserEditSerializer(user)
        if request.method == 'PATCH':
            serializer = UserEditSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(AdminViewSet):
    """View представления категорий на кастомном миксине"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AdminViewSet):
    """View представления жанров на кастомном миксине"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """View представления произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlePostSerialzier
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """View представления оценок."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeRatOrOrAdminOrReadOnly,)

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
    """View представления комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeRatOrOrAdminOrReadOnly,)

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
