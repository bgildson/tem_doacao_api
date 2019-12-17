from rest_framework.serializers import ModelSerializer

from .models import Specie


class SpecieSerializer(ModelSerializer):
    class Meta:
        model = Specie
        fields = (
            'id', 'name', 'created_at',
        )
        read_only_fields = fields
