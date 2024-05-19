from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from apps.roles.models import Roles

class GroupPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Fetch all permissions associated with roles the user belongs to
        user_roles = Roles.objects.filter(user=request.user)
        user_permissions = Permission.objects.filter(
            group__in=user_roles
        ).values_list('codename', flat=True)
        
        # Define required permissions for the view
        required_permissions = getattr(view, 'required_permissions', [])
        
        # Check if the user has all required permissions for the view
        return all(permission in user_permissions for permission in required_permissions)




