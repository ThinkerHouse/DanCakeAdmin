from django.db import models
from django.utils import timezone

from config.util.constants.constants import ACTIVE_STATUS_CHOICES


class Product(models.Model):
    class Meta:
        db_table = 'products'

    name = models.CharField(max_length=50, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=ACTIVE_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(blank=True, null=True)  # Can be null initially

    def save(self, *args, **kwargs):
        if self.pk is not None:  # If object is being updated
            self.updated_at = timezone.now()
        elif not self.created_at:  # If object is being created
            self.created_at = timezone.now()
        return super(Product, self).save(*args, **kwargs)