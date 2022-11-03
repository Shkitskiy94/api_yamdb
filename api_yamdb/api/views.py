from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Title

from .permissions import (IsAdminModeratorOwnerOrReadOnly)
from .serializers import (ReviewSerializer, CommentSerializer)

from .permissions import (IsAdminOrReadOnly)
from .mixins import CreateListDeleteViewSet
from .filters import TitleFilter


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