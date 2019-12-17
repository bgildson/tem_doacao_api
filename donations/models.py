import uuid

from django.db import models

from core.utils import generic_upload_to


def donations_images_upload_to(instance, filename):
    return generic_upload_to('donations-images', instance, filename)


class Donation(models.Model):
    STARTED = 'started'
    FINALIZED = 'finalized'
    STOPPED = 'stopped'
    CANCELED = 'canceled'
    STATUS = (
        (STARTED, STARTED),
        (FINALIZED, FINALIZED),
        (STOPPED, STOPPED),
        (CANCELED, CANCELED),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.CharField(max_length=128)
    long_description = models.TextField()
    category = models.ForeignKey('categories.Category', db_column='category_id',
                                 on_delete=models.SET_NULL, null=True)
    donor = models.ForeignKey('users.User', db_column='user_id_donor',
                              on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=16, choices=STATUS, default=STARTED)
    started_at = models.DateTimeField(auto_now_add=True)
    finalized_at = models.DateTimeField(null=True)
    canceled_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)


class DonationImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    image = models.ImageField(upload_to=donations_images_upload_to, null=True)
    donation = models.ForeignKey('donations.Donation', db_column='donation_id',
                                 related_name='images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
