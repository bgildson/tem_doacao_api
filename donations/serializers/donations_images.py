from rest_framework import serializers

from ..models import Donation, DonationImage


class DonationImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, allow_null=False)
    donation_id = serializers.PrimaryKeyRelatedField(source='donation',
                                                     required=True,
                                                     queryset=Donation.objects.all())

    class Meta:
        model = DonationImage
        fields = (
            'id', 'image', 'donation_id', 'created_at',
        )
        read_only_fields = (
            'id', 'created_at',
        )
