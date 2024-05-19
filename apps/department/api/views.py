from rest_framework import generics
from apps.department.api.serializers import DepartmentSerializer
from apps.department.models import Department
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission

class DepartmentListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_department', 'add_department']
    queryset = Department.objects.all().order_by('id')

    def get_serializer_class(self):
        return DepartmentSerializer
    
    def list(self, request, *args, **kwargs):
        return self.custom_list_response(
            queryset=self.get_queryset(),
            serializer_class=self.get_serializer_class()
        )
    
    def create(self, request, *args, **kwargs):
        return CustomListCreateMixin.create(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.GET.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return self.filter_queryset(queryset, name='name', status='status')

class DepartmentRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_department', 'delete_department']
    queryset = Department.objects.all()

    def get_serializer_class(self):
        return DepartmentSerializer
    
    def retrieve(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.destroy(self, request, *args, **kwargs)
