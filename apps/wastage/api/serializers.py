from attr import field
from rest_framework import serializers
from config.util.serializers.serializers_utils import get_created_by, get_updated_by, get_approved_by
from apps.wastage.models import Wastage

class WastageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    approved_by_info = serializers.SerializerMethodField(read_only=True)
    updated_by_info = serializers.SerializerMethodField(read_only=True)
    created_by_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wastage
        fields = ['id', 'item_id', 'item_name', 'reference_id', 'quantity', 'batch_no', 'unit', 'remarks', 'wastage_from', 'wastage_type', 'created_by', 'created_by_info', 'updated_by', 'updated_by_info', 'approved_by', 'approved_by_info', 'created_at', 'updated_at']
    
    def validate_item_name(self, value):
        if len(value) < 3 or len(value) > 150:
            raise serializers.ValidationError("Item Name must be between 3 and 150 characters long.")
        return value
    
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y %I:%M %p")

    def get_updated_at(self, instance):
        updated_at = instance.updated_at
        return updated_at.strftime("%B %d, %Y %I:%M %p") if updated_at else None
    
    def get_updated_by_info(self, instance):
        return get_updated_by(instance)

    def get_created_by_info(self, instance):
        return get_created_by(instance)
    
    def get_approved_by_info(self, instance):
        return get_approved_by(instance)