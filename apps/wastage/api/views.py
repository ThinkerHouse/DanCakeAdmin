from rest_framework import generics
from apps.material_type.api.serializers import MaterialTypeSerializer
from apps.material_type.models import MaterialType
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission

class MaterialTypeListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin,generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_materialtype', 'add_materialtype']
    queryset = MaterialType.objects.all().order_by('id')

    def get_serializer_class(self):
        return MaterialTypeSerializer
    
    def list(self, request, *args, **kwargs):
        return self.custom_list_response(
            queryset=self.get_queryset(),
            serializer_class=self.get_serializer_class()
        )
    
    def create(self, request, *args, **kwargs):
        return CustomListCreateMixin.create(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset, name='name', status='status')

class MaterialTypeRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_materialtype', 'delete_materialtype']
    queryset = MaterialType.objects.all()

    def get_serializer_class(self):
        return MaterialTypeSerializer
    
    def retrieve(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.destroy(self, request, *args, **kwargs)
