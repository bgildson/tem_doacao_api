import uuid

from django.db import models

from core.utils import generic_upload_to


class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    donation = models.ForeignKey('donations.Donation', db_column='donation_id',
                                 on_delete=models.SET_NULL, null=True,
                                 related_name='favorites')
    user = models.ForeignKey('users.User', db_column='user_id_donor',
                             on_delete=models.SET_NULL, null=True,
                             related_name='favorites')
    at = models.DateTimeField(auto_now_add=True)
