from django.db import models
from django.utils import timezone

from apps.material_type.models import MaterialType
from apps.unit.models import Unit
from config.util.constants.constants import ACTIVE_STATUS_CHOICES, STORAGE_TYPE_CHOICE


class Material(models.Model):
    class Meta:
        db_table = 'materials'

    unit = models.ForeignKey(Unit, related_name='unit', on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, related_name='material_type', on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50, unique=True)
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPE_CHOICE, default='regular')
    status = models.IntegerField(choices=ACTIVE_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updated_at = timezone.now()
        elif not self.created_at:
            self.created_at = timezone.now()
        return super(Material, self).save(*args, **kwargs)