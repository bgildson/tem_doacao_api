import json

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.utils.translation import ugettext as _
from drf_yasg.utils import swagger_auto_schema
import requests
from rest_framework import generics, serializers, status
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, SignInSerializer, SignInUpSerializer


class SignInUpView(APIView):
    @swagger_auto_schema(query_serializer=SignInUpSerializer,
                         responses={200: SignInSerializer()},)
    @transaction.atomic()
    def post(self, request):
        sign_in_up_serializer = SignInUpSerializer(data=request.data)

        sign_in_up_serializer.is_valid()

        token = sign_in_up_serializer.data['social_auth_google_token']

        if not token:
            raise serializers.ValidationError(_('Token não informado!'))

        userinfo_url = f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={token}'
        response_userinfo = requests.get(userinfo_url)

        if response_userinfo.status_code != 200:
            msg = _('Não foi possível fazer o login, token inválido!')
            raise serializers.ValidationError(msg)

        user_google = json.loads(response_userinfo.text)

        user = get_user_model().objects \
            .filter(social_auth_google_id=user_google['id']) \
            .first()

        if not user:
            response_user_picture = requests.get(user_google['picture'])
            filename = response_user_picture.headers \
                .get('content-disposition', '') \
                .split('filename="')[-1] \
                .split('"')[0]
            content_type = response_user_picture.headers.get('content-type')
            photo = SimpleUploadedFile(filename,
                                       response_user_picture.content,
                                       content_type=content_type)
            user_data = {
                'username': get_user_model().objects.make_random_username(), # required
                'name': user_google['name'],
                'photo': photo,
                'email': user_google['email'],
                'social_auth_google_id': user_google['id'],
            }
            user = get_user_model().objects.create_user(**user_data)
            user.save()

        payload = jwt_payload_handler(user)

        user_serializer = UserSerializer(instance=user)

        response_data = {
            'token': jwt_encode_handler(payload),
            'user': user_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
