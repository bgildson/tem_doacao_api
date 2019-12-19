from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoritesSwaggerSchema(SwaggerAutoSchema):
    def get_security(self):
        if self.view.action in ('list', 'retrieve',):
            return []
        return super().get_security()


class FavoritesViewSet(ReadOnlyModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('donation__id',)
    ordering = ('-at',)
    swagger_schema = FavoritesSwaggerSchema

    def get_queryset(self):
        return Favorite.objects \
            .filter(user=self.request.user) \
            .all()
