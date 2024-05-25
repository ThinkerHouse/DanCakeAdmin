from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.unit.models import Unit
from config.util.constants.constants import WASTAGE_FROM_CHOICE, WASTAGE_TYPE_CHOICE


class Wastage(models.Model):
    class Meta:
        db_table = 'wastages'

    unit = models.ForeignKey(Unit, related_name='wastage_unit', on_delete=models.CASCADE)
    
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=50)
    reference_id = models.CharField(max_length=50)
    quantity = models.IntegerField()
    batch_no = models.CharField(max_length=50)
    remarks = models.TextField()
    wastage_from = models.CharField(max_length=20, choices=WASTAGE_FROM_CHOICE, default='production')
    wastage_type = models.CharField(max_length=20, choices=WASTAGE_TYPE_CHOICE, default='regular')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wastage_created_by')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wastage_approved_by', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wastage_updated_by', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updated_at = timezone.now()
        elif not self.created_at:
            self.created_at = timezone.now()
        return super(Wastage, self).save(*args, **kwargs)