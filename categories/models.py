import uuid

from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
