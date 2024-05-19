import re
from rest_framework import serializers
from apps.check_list.models import CheckList

class CheckListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = CheckList
        fields = ['id', 'name', 'type', 'status', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        return self._validate_string(value, 3, 300)

    def _validate_string(self, value, min_length=2, max_length=100):
        if len(value) < min_length or len(value) > max_length:
            raise serializers.ValidationError("Name must be between 3 and 300 characters long.")
        if not re.match(r'^[a-zA-Z0-9\s]*[-_&]*[a-zA-Z0-9\s]*$', value):
            raise serializers.ValidationError("Name must contain only alphanumeric characters, hyphens (-), underscores (_), and ampersands (&).")
        return value
    
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y %I:%M %p")

    def get_updated_at(self, instance):
        updated_at = instance.updated_at
        return updated_at.strftime("%B %d, %Y %I:%M %p") if updated_at else None