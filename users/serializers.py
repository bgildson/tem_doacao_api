import json

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    photo_url = serializers.ImageField(source='photo', allow_null=True, required=False)

    class Meta:
        model = User
        fields = (
            'id', 'name', 'photo_url', 'created_at',
        )
        read_only_fields = fields


class SignInUpSerializer(serializers.Serializer):
    social_auth_google_token = serializers.CharField(required=True)


class SignInSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()
