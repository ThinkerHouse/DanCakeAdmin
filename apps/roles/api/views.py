from rest_framework import generics
from apps.roles.models import Roles
from django.contrib.auth.models import Permission
from .serializers import RolesSerializer, PermissionsSerializer, RolesDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.permissions.GroupPermission import GroupPermission

class RolesListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    """
    API view for listing and creating roles.
    """
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_roles', 'add_roles']
    queryset = Roles.objects.all().order_by('id')

    def get_serializer_class(self):
        return RolesSerializer
    
    def list(self, request, *args, **kwargs):
        return self.custom_list_response(
            queryset=self.get_queryset(),
            serializer_class=self.get_serializer_class(),
            message="Role list retrieved successfully"
        )
        
    def create(self, request, *args, **kwargs):
        return CustomListCreateMixin.create(self, request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset, name='name')
    
class RolesRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView, CustomRetrieveUpdateDestroyMixin):
    """
    API view for retrieving, updating, and deleting a role.
    """
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_roles', 'delete_roles']
    queryset = Roles.objects.all()
    
    def get_serializer_class(self):
        return RolesSerializer
    
    def retrieve(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.update(self, request, *args, **kwargs)


class PermissionListView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    """
    API view for listing permissions.
    """
    permission_classes = [IsAuthenticated]
    required_permissions = ['view_permission']
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionsSerializer
    
    def list(self, request, *args, **kwargs):
        return self.custom_list_response(
            queryset=self.get_queryset(),
            serializer_class=self.get_serializer_class(),
            message="Permission list retrieved successfully"
        )
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset, name='name', codename="codename")