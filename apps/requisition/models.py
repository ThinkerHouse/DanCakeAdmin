import datetime
from django.db import models
from apps.users.models import User
from apps.unit.models import Unit
from apps.department.models import Department
from apps.production.models import Production
from apps.material.models import Material
from config.util.constants.constants import APPROVAL_STATUS_CHOICE


class Requisition(models.Model):
    class Meta:
        db_table = 'requisitions'

    batch_no = models.CharField(max_length=255, unique=True, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="requisition_department")
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name="requisition_production")
    date_requested = models.DateTimeField(blank=True, null=True)
    expected_delivery_date = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True)
    purpose = models.CharField(choices=APPROVAL_STATUS_CHOICE, default='pending')
    status = models.CharField(choices=APPROVAL_STATUS_CHOICE, default='pending')
    meta_data = models.JSONField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requisition_created_by')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requisition_approved_by', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requisition_updated_by', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    # Override the save method to set the batch_no if it's not set
    def save(self, *args, **kwargs):
        if not self.batch_no:
            now = datetime.datetime.now()
            # Example format: DCPBYYYYMMDDHHMMSS
            batch_no = f"DCRQ{now.strftime('%Y%m%d%H%M%S')}"
            self.batch_no = batch_no
        super().save(*args, **kwargs)
    
    
class RequisitionItem(models.Model):
    class Meta:
        db_table = 'requisition_items'
        
    requisition = models.ForeignKey(Requisition, related_name="requisition_items", on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, related_name='requisition_unit_info', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name='requisition_material_info', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    
