from rest_framework import generics
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission
from apps.returns.api.serializers import ReturnsSerializer, ReturnItemSerializer
from apps.returns.models import Returns, ReturnItem

class ReturnsListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['view_production', 'add_production']
    queryset = Returns.objects.all().order_by('id')

    def get_serializer_class(self):
        return ReturnsSerializer

    def list(self, request, *args, **kwargs):
        return self.custom_list_response(
            queryset=self.get_queryset(),
            serializer_class=self.get_serializer_class()
        )

    def create(self, request, *args, **kwargs):
        return CustomListCreateMixin.create(self, request, *args, **kwargs)
    
    # Overrider perform create method to set requested user
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

class ReturnsRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['change_checklist', 'delete_checklist']
    queryset = Returns.objects.all()

    def get_serializer_class(self):
        return ReturnsSerializer
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)