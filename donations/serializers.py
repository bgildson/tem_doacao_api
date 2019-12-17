from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from users.serializers import UserSerializer
from .models import Donation, DonationImage


class DonationSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(source='category', required=True,
                                                     queryset=Category.objects.all())
    category = CategorySerializer(read_only=True)
    donor = UserSerializer(read_only=True)
    images = serializers.SlugRelatedField(many=True, slug_field='image',
                                          read_only=True)

    class Meta:
        model = Donation
        fields = (
            'id', 'description', 'long_description', 'category_id',
            'category', 'donor', 'status', 'images', 'started_at',
            'finalized_at', 'canceled_at', 'updated_at',
        )
        read_only_fields = (
            'id', 'category', 'donor', 'status', 'images', 'started_at',
            'finalized_at', 'canceled_at', 'updated_at',
        )
        extra_kwargs = {'donor': {'default': serializers.CurrentUserDefault()}}
