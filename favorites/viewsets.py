from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Favorite
from .serializers import FavoriteSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(security=[]))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(security=[]))
class FavoritesViewSet(ReadOnlyModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('donation__id',)
    ordering = ('-at',)

    def get_queryset(self):
        return Favorite.objects \
            .filter(user=self.request.user) \
            .all()
