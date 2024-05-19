from django.db import models
from apps.users.models import User
from apps.purchase_order.models import PurchaseOrder, PurchaseOrderItem
from config.util.constants.constants import RECEIVED_ORDER_STATUS_CHOICE, STORAGE_TYPE_CHOICE

class ReceivedOrder(models.Model):
    class Meta:
        db_table = 'received_orders'

    batch_no = models.CharField(max_length=255)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="received_order_purchase_order")
    received_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True)
    meta_data = models.JSONField(blank=True, null=True,)
    status = models.CharField(choices=RECEIVED_ORDER_STATUS_CHOICE, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_order_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_order_updated_by', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    
    
class ReceivedOrderItem(models.Model):
    class Meta:
        db_table = 'received_order_items'
        
    received_order = models.ForeignKey(ReceivedOrder, related_name="received_order_items", on_delete=models.CASCADE)
    purchase_order_item = models.ForeignKey(PurchaseOrderItem, related_name='ro_purchase_order_item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    storage_condition = models.CharField(choices=STORAGE_TYPE_CHOICE, default='regular')

