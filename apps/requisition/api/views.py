from rest_framework import generics, status as http_status
from rest_framework.exceptions import ValidationError
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission
from apps.requisition.api.serializers import RequisitionSerializer, RequisitionItemSerializer
from apps.requisition.models import Requisition, RequisitionItem
from config.util.response_handler.custom_response_handler import custom_response_handler as custom_resp_hand

class RequisitionListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['view_production', 'add_production']
    queryset = Requisition.objects.all().order_by('id')

    def get_serializer_class(self):
        return RequisitionSerializer

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

class RequisitionRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['change_checklist', 'delete_checklist']
    queryset = Requisition.objects.all()

    def get_serializer_class(self):
        return RequisitionSerializer
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class RequisitionItemCreateAPIView(CustomListCreateMixin, generics.CreateAPIView):
    serializer_class = RequisitionItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        requisition_id = self.kwargs['requisition_id']
        try:
            requisition = Requisition.objects.get(id=requisition_id)
        except Requisition.DoesNotExist:
            raise ValidationError("Requisition not found.")

        if requisition.status == 'approved' and requisition.approved_by is not None:
            raise ValidationError("Cannot create item for an approved requisition.")

        serializer.save(requisition=requisition)

# Generic view to delete RequisitionItem
class RequisitionItemDeleteAPIView(CustomRetrieveUpdateDestroyMixin, generics.DestroyAPIView):
    queryset = RequisitionItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RequisitionItemSerializer

    def perform_destroy(self, instance):
        requisition_id = instance.requisition.id
        requisition = Requisition.objects.get(id=requisition_id)
        if requisition.status == 'approved' and requisition.approved_by is not None:
            return custom_resp_hand({}, status=http_status.HTTP_200_OK, message="Cannot delete item from an approved requisition.")
        instance.delete()