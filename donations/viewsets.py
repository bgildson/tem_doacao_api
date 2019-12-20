from django.db import transaction
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import mixins, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from .models import Donation, DonationImage
from .pagination import DonationsPagination
from .permissions import DonationsPermission, DonationsImagesPermission
from .serializers.donations import DonationSerializer
from .serializers.donations_images import DonationImageSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(security=[]))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(security=[]))
class DonationsViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly & DonationsPermission,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    filterset_fields = ('category__id',)
    search_fields = ('description', 'long_description', 'category__name',)
    # default ordering, required by cursor pagination style
    ordering = ('-started_at',)
    pagination_class = DonationsPagination

    @swagger_auto_schema(responses={200: FavoriteSerializer(), 204: ''},
                         request_body=no_body)
    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated,))
    @transaction.atomic()
    def toggle_favorite(self, request, pk, *args, **kwargs):
        donation = self.get_object()
        favorite = Favorite.objects.filter(donation=donation, user=request.user).first()

        if favorite:
            favorite.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = FavoriteSerializer(data={'donation_id': pk},
                                            context={'request': request})
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: FavoriteSerializer()}, request_body=no_body)
    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated,))
    @transaction.atomic()
    def favorite(self, request, pk, *args, **kwargs):
        donation = self.get_object()
        favorite = Favorite.objects.filter(donation__id=pk, user=request.user).first()

        if favorite:
            serializer = FavoriteSerializer(instance=favorite)
        else:
            serializer = FavoriteSerializer(data={'donation_id': pk},
                                            context={'request': request})
            serializer.is_valid()
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={204: ''}, request_body=no_body)
    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated,))
    @transaction.atomic()
    def unfavorite(self, request, pk, *args, **kwargs):
        donation = self.get_object()
        favorite = Favorite.objects.filter(donation__id=pk, user=request.user).first()

        if favorite:
            favorite.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


@method_decorator(name='list', decorator=swagger_auto_schema(security=[]))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(security=[]))
class DonationsImagesViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = DonationImage.objects.all()
    serializer_class = DonationImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly & DonationsImagesPermission,)
