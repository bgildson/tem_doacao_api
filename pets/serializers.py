from rest_framework import serializers

from species.serializers import SpecieSerializer
from users.serializers import UserSerializer
from .models import Pet, PetImage


class PetSerializer(serializers.ModelSerializer):
    specie = SpecieSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    images = serializers.SlugRelatedField(many=True, slug_field='photo', queryset=PetImage.objects.all())

    class Meta:
        model = Pet
        fields = (
            'id', 'name', 'born_at', 'description', 
            'specie', 'user', 'images', 'created_at',
        )
        read_only_fields = ('id', 'created_at',)
