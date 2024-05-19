from attr import field
from rest_framework import serializers

from apps.material_type.models import MaterialType

class MaterialTypeSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = MaterialType
        fields = ['id', 'name', 'status', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        if len(value) < 3 or len(value) > 50:
            raise serializers.ValidationError("Name must be between 3 and 50 characters long.")
        return value
    
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y %I:%M %p")

    def get_updated_at(self, instance):
        updated_at = instance.updated_at
        return updated_at.strftime("%B %d, %Y %I:%M %p") if updated_at else None