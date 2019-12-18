from django.db import transaction
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import mixins, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from .models import Donation, DonationImage
from .permissions import DonationsPermission, DonationsImagesPermission
from .serializers import DonationSerializer, DonationImageSerializer


class DonationsViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Donation.objects.order_by('-started_at').all()
    serializer_class = DonationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly & DonationsPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('description', 'long_description', 'category__name',)

    @swagger_auto_schema(responses={200: FavoriteSerializer()}, request_body=no_body)
    @action(methods=['post'], detail=True)
    @transaction.atomic()
    def toggle_favorite(self, request, pk, *args, **kwargs):
        favorite = Favorite.objects.filter(donation__id=pk, user=request.user).first()

        if favorite:
            favorite.delete()
            response_data = None
        else:
            serializer = FavoriteSerializer(data={'donation_id': pk}, context={'request': request})
            serializer.is_valid()
            serializer.save()
            response_data = serializer.data

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: FavoriteSerializer()}, request_body=no_body)
    @action(methods=['post'], detail=True)
    @transaction.atomic()
    def favorite(self, request, pk, *args, **kwargs):
        favorite = Favorite.objects.filter(donation__id=pk, user=request.user).first()

        if favorite:
            serializer = FavoriteSerializer(instance=favorite)
        else:
            serializer = FavoriteSerializer(data={'donation_id': pk}, context={'request': request})
            serializer.is_valid()
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={204: ''}, request_body=no_body)
    @action(methods=['post'], detail=True)
    @transaction.atomic()
    def unfavorite(self, request, pk, *args, **kwargs):
        favorite = Favorite.objects.filter(donation__id=pk, user=request.user).first()

        if favorite:
            favorite.delete()

        return Response(None, status=status.HTTP_204_OK)


class DonationsImagesViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = DonationImage.objects.all()
    serializer_class = DonationImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly & DonationsImagesPermission,)
