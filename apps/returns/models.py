from django.db import models
from apps.users.models import User
from config.util.constants.constants import RETURN_STATUS_CHOICE, RETURN_TYPE_CHOICE

class Returns(models.Model):
    class Meta:
        db_table = 'returns'

    return_type = models.CharField(choices=RETURN_TYPE_CHOICE, default='material')
    referance_id = models.CharField(max_length=50, unique=True)
    return_to = models.CharField(max_length=50, blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=RETURN_STATUS_CHOICE, default='pending')
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='return_created_by')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='return_approved_by', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='return_updated_by', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    
    
class ReturnItem(models.Model):
    class Meta:
        db_table = 'return_items'
        
    returns = models.ForeignKey(Returns, related_name="return_items", on_delete=models.CASCADE)
    item_id = models.CharField(max_length=50)
    quantity = models.IntegerField()

    
