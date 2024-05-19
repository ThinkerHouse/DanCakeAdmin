from tokenize import group
from rest_framework import serializers
from apps.users.models import User
from apps.roles.api.serializers import RolesSerializer, PermissionsSerializer, RolesDetailsSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.users.models import User

from django.utils import timezone
from django.contrib.auth.models import Group


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(
        read_only=True, default=timezone.now)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'user_permissions': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', '123456')
        groups_data = validated_data.pop('groups', [])
        validated_data.pop('user_permissions')

        if password is not None:
            # Encrypt the password
            validated_data['password'] = make_password(password)


        user = User.objects.create(**validated_data)
        # Handle many-to-many relationship with groups
        for group_data in groups_data:
            user.groups.add(group_data)

        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        groups_data = validated_data.pop('groups', None)

        if password:
            # Encrypt the password
            validated_data['password'] = make_password(password)

        # Update user instance with validated data
        instance = super().update(instance, validated_data)

        # Handle many-to-many relationship with groups
        if groups_data is not None:
            instance.groups.set(groups_data)

        return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    groups = RolesDetailsSerializer(many=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'user_permissions': {'write_only': True}
        }
