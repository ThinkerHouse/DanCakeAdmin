from rest_framework import generics
# from apps.department.api.serializers import DepartmentSerializer
from apps.department.models import Department
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission

from apps.purchase_order.api.serializers import PurchaseOrderSerializer
from apps.purchase_order.models import PurchaseOrder, PurchaseOrderItem


class PurchaseOrderListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['view_department', 'add_department']
    queryset = PurchaseOrder.objects.all().order_by('id')

    def get_serializer_class(self):
        return PurchaseOrderSerializer

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


class PurchaseOrderRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['change_checklist', 'delete_checklist']
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self):
        return PurchaseOrderSerializer
    
    # Overrider perform create method to set requested user
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

