from rest_framework import serializers

from donations.serializers import DonationSerializer
from users.serializers import UserSerializer
from donations.models import Donation
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    donation_id = serializers.PrimaryKeyRelatedField(source='donation',
                                                     required=True,
                                                     write_only=True,
                                                     queryset=Donation.objects.all())
    donation = DonationSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = (
            'id', 'donation_id', 'donation', 'user', 'at',
        )
        read_only_fields = (
            'id', 'donation', 'user', 'at',
        )

    def create(self, validated_data):
        return super(FavoriteSerializer, self) \
            .create({**validated_data, 'user': self.context['request'].user})
