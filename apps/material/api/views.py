from rest_framework import generics
from apps.material.api.serializers import MaterialSerializer
from apps.material.models import Material
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission

class MaterialListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin,generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_material', 'add_material']
    queryset = Material.objects.all().order_by('id')

    def get_serializer_class(self):
        return MaterialSerializer
    
    def list(self, request, *args, **kwargs):
        return self.custom_list_response(
            queryset=self.get_queryset(),
            serializer_class=self.get_serializer_class()
        )
    
    def create(self, request, *args, **kwargs):
        return CustomListCreateMixin.create(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {
            'unit_id': 'unit_id',
            'material_type_id': 'material_type_id',
        }

        # Iterate over the filter parameters and apply filters to the queryset
        for param, field in filter_params.items():
            value = self.request.GET.get(param)
            if value:
                queryset = queryset.filter(**{field: value})

        return self.filter_queryset(queryset, name='name', storage_type='storage_type', status='status')

class MaterialRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_material', 'delete_material']
    queryset = Material.objects.all()

    def get_serializer_class(self):
        return MaterialSerializer
    
    def retrieve(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.destroy(self, request, *args, **kwargs)
