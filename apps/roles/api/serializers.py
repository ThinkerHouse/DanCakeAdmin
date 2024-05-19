from rest_framework import serializers
from apps.roles.models import Roles
from django.contrib.auth.models import Permission


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionsRelatedFieldSerializer(serializers.StringRelatedField):
    def to_representation(self, value):
        return super().to_representation(value)


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class RolesDetailsSerializer(serializers.ModelSerializer):
    # permissions = PermissionsRelatedFieldSerializer(many=True)

    class Meta:
        model = Roles
        fields = '__all__'
