import re
from rest_framework import serializers
from apps.production_plant.models import ProductionPlant
    
class ProductionPlantSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductionPlant
        fields = ['id', 'user', 'user_info', 'name', 'description', 'location', 'capacity', 'status', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        return self._validate_field(value, 3, 50)
    
    def validate_capacity(self, value):
        return self._validate_field(value, 3, 50)

    def _validate_field(self, value, min_length=2, max_length=100):
        if len(value) < min_length or len(value) > max_length:
            raise serializers.ValidationError(f"Field must be between {min_length} and {max_length} characters long.")
        if not re.match(r'^[a-zA-Z0-9\s]*[-_&]*[a-zA-Z0-9\s]*$', value):
            raise serializers.ValidationError("Field must contain only alphanumeric characters, hyphens (-), underscores (_), and ampersands (&).")
        return value
    
    def get_user_info(self, instance):
        return {
            'id': instance.user.id,
            'name': instance.user.first_name +" "+ instance.user.last_name,
            'username': instance.user.username
        }
    
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y %I:%M %p")

    def get_updated_at(self, instance):
        updated_at = instance.updated_at
        return updated_at.strftime("%B %d, %Y %I:%M %p") if updated_at else None
    