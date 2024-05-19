from django.db import models
from django.utils import timezone
from config.util.constants.constants import ACTIVE_STATUS_CHOICES


class Unit(models.Model):
    class Meta:
        db_table = 'units'

    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    status = models.IntegerField(choices=ACTIVE_STATUS_CHOICES, default=0)
    # Automatically set on creation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        blank=True, null=True)  # Can be null initially

    def save(self, *args, **kwargs):
        if self.pk is not None:  # If object is being updated
            self.updated_at = timezone.now()
        elif not self.created_at:  # If object is being created
            self.created_at = timezone.now()
        return super(Unit, self).save(*args, **kwargs)
