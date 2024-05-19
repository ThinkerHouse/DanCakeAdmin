from rest_framework import serializers
from apps.material.models import Material
import re

class MaterialSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    unit_info = serializers.SerializerMethodField(read_only=True)
    material_type_info = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Material
        fields = ['id', 'unit', 'unit_info', 'material_type', 'material_type_info', 'name', 'storage_type', 'status', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        return self._validate_string_field(value, 3, 50)

    def storage_type(self, value):
        return self._validate_string_field(value, 3, 50)
    
    def _validate_string_field(self, value, min_length=2, max_length=100):
        if len(value) < min_length or len(value) > max_length:
            raise serializers.ValidationError("Name must be between 3 and 50 characters long.")
        if not re.match(r'^[a-zA-Z0-9\s]*[-_&]*[a-zA-Z0-9\s]*$', value):
            raise serializers.ValidationError("Name must contain only alphanumeric characters, hyphens (-), underscores (_), and ampersands (&).")
        return value
    
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y %I:%M %p")

    def get_updated_at(self, instance):
        updated_at = instance.updated_at
        return updated_at.strftime("%B %d, %Y %I:%M %p") if updated_at else None
    
    def get_unit_info(self, instance):
        return {
            'id': instance.unit.id,
            'name': instance.unit.name
        }
    
    def get_material_type_info(self, instance):
        return {
            'id': instance.material_type.id,
            'name': instance.material_type.name 
        }
