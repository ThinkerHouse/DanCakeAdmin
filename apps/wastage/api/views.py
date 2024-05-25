from rest_framework import generics
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission
from apps.wastage.api.serializers import WastageSerializer
from apps.wastage.models import Wastage
from config.util.response_handler.custom_response_handler import custom_response_handler as custom_resp_hand

class WastageListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_wastage', 'add_wastage']
    queryset = Wastage.objects.all().order_by('id')

    def get_serializer_class(self):
        return WastageSerializer

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

class WastageRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_wastage', 'delete_wastage']
    queryset = Wastage.objects.all()

    def get_serializer_class(self):
        return WastageSerializer
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)