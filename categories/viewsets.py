from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Category
from .serializers import CategorySerializer


class CategoriesViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.order_by('name').all()
    serializer_class = CategorySerializer
