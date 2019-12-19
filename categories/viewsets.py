from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_yasg.inspectors import SwaggerAutoSchema

from .models import Category
from .serializers import CategorySerializer


class CategoriesSwaggerSchema(SwaggerAutoSchema):
    def get_security(self):
        if self.view.action in ('list', 'retrieve',):
            return []
        return super().get_security()


class CategoriesViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.order_by('name').all()
    serializer_class = CategorySerializer
    swagger_schema = CategoriesSwaggerSchema
