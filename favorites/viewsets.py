from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoritesViewSet(ReadOnlyModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('donation__id',)
    ordering = ('-at',)

    def get_queryset(self):
        return Favorite.objects \
            .filter(user=self.request.user) \
            .all()
