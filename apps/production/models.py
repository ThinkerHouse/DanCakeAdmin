import datetime
from django.db import models
from apps.users.models import User
from apps.unit.models import Unit
from apps.product.models import Product
from apps.production_plant.models import ProductionPlant
from config.util.constants.constants import APPROVAL_STATUS_CHOICE


class Production(models.Model):
    class Meta:
        db_table = 'productions'

    name = models.CharField(max_length=255, unique=True)
    batch_no = models.CharField(max_length=255, unique=True, blank=True, null=True)
    production_plant = models.ForeignKey(ProductionPlant, on_delete=models.CASCADE, related_name="proudction_plant")
    expected_delivery_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    remarks = models.TextField(blank=True)
    status = models.CharField(choices=APPROVAL_STATUS_CHOICE, default='pending')
    meta_data = models.JSONField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='production_created_by')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='production_approved_by', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='production_updated_by', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    # Override the save method to set the batch_no if it's not set
    def save(self, *args, **kwargs):
        if not self.batch_no:
            now = datetime.datetime.now()
            # Example format: DCPBYYYYMMDDHHMMSS
            batch_no = f"DCPB{now.strftime('%Y%m%d%H%M%S')}"
            self.batch_no = batch_no
        super().save(*args, **kwargs)
    
    
class ProductionItem(models.Model):
    class Meta:
        db_table = 'production_items'
        
    production = models.ForeignKey(Production, related_name="production_items", on_delete=models.CASCADE)
    # unit = models.ForeignKey(Unit, related_name='unit_info', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_info', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    
