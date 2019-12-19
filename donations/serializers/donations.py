from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from users.serializers import UserSerializer
from ..models import Donation


class DonationImageSerializer(serializers.Serializer):
    id = serializers.CharField()
    image_url = serializers.ImageField(source='image')

    class Meta:
        ref_name = None


class DonationSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(source='category', required=True,
                                                     queryset=Category.objects.all())
    category = CategorySerializer(read_only=True)
    donor = UserSerializer(read_only=True)
    images = DonationImageSerializer(many=True, read_only=True)

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

    def create(self, validated_data):
        return super(DonationSerializer, self) \
            .create({**validated_data, 'donor': self.context['request'].user})
