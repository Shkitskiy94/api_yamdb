from rest_framework import viewsets

from reviews.models import (
    Category, Genre,
    Title
)
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializerForWrite,
    TitleSerializerForView,
)
from .permissions import (IsAdminOrReadOnly)
from .mixins import CreateListDeleteViewSet
from .filters import TitleFilter

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