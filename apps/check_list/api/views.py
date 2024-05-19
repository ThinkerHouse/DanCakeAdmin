from rest_framework import generics
from apps.check_list.api.serializers import CheckListSerializer
from apps.check_list.models import CheckList
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission

class CheckListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_checklist', 'add_checklist']
    queryset = CheckList.objects.all().order_by('id')

    def get_serializer_class(self):
        return CheckListSerializer
    
    def list(self, request, *args, **kwargs):
        return self.custom_list_response(
            queryset=self.get_queryset(),
            serializer_class=self.get_serializer_class()
        )
    
    def create(self, request, *args, **kwargs):
        return CustomListCreateMixin.create(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset, name='name', type='type', status='status')

class CheckListRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_checklist', 'delete_checklist']
    queryset = CheckList.objects.all()

    def get_serializer_class(self):
        return CheckListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return CustomRetrieveUpdateDestroyMixin.destroy(self, request, *args, **kwargs)
