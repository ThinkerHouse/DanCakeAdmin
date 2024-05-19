from django.db import models
from apps.users.models import User
from apps.material.models import Material
from config.util.constants.constants import APPROVAL_STATUS_CHOICE


class PurchaseOrder(models.Model):
    class Meta:
        db_table = 'purchase_order'

    tracking_id = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchased_vendor")
    order_date = models.DateField()
    expected_delivery_date = models.DateField(blank=True)
    delivered_at = models.DateTimeField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True)
    meta_data = models.TextField(blank=True)
    status = models.CharField(choices=APPROVAL_STATUS_CHOICE, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_updated_by', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    
    
class PurchaseOrderItem(models.Model):
    class Meta:
        db_table = 'purchase_order_item'
        
    purchase_order = models.ForeignKey(PurchaseOrder, related_name="purchase_order_items", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name='material_info', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    
