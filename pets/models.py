import uuid

from django.db import models


def pets_upload_to(instance, filename):
    return generic_upload_to('pets', instance, filename)


class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128)
    born_at = models.DateTimeField()
    description = models.TextField()
    specie = models.ForeignKey('species.Specie', db_column='specie_id',
                               on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('users.User', db_column='user_id',
                             on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PetImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    photo = models.ImageField(upload_to=pets_upload_to, null=True)
    pet = models.ForeignKey('pets.Pet', db_column='pet_id', related_name='images',
                            on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
