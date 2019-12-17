import uuid

from django.db import models
from django.contrib.auth import models as auth_models

from core.utils import generic_upload_to


def users_upload_to(instance, filename):
    return generic_upload_to('users', instance, filename)


class UserManager(auth_models.UserManager):
    def make_random_username(self):
        while True:
            username = f'User_{self.make_random_password(8)}'
            if not self.model.objects.filter(username=username):
                return username


class User(auth_models.AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128)
    photo = models.ImageField(upload_to=users_upload_to, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    social_auth_google_id = models.CharField(max_length=64, null=True)

    objects = UserManager()
