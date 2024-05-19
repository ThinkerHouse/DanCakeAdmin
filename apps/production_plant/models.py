from django.db import models
from django.utils import timezone
from apps.users.models import User

from config.util.constants.constants import ACTIVE_STATUS_CHOICES


class ProductionPlant(models.Model):
    class Meta:
        db_table = 'production_plants'

    user = models.ForeignKey(
        User, related_name='production_plant_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    location = models.TextField(blank=True)
    capacity = models.CharField(max_length=50)
    status = models.IntegerField(choices=ACTIVE_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updated_at = timezone.now()
        elif not self.created_at:
            self.created_at = timezone.now()
        return super(ProductionPlant, self).save(*args, **kwargs)