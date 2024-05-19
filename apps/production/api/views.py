from rest_framework import generics, status as http_status
from apps.department.models import Department
from rest_framework.exceptions import ValidationError
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission
from apps.production.api.serializers import ProductionItemSerializer, ProductionSerializer
from apps.production.models import Production, ProductionItem
from config.util.response_handler.custom_response_handler import custom_response_handler as custom_resp_hand

class ProductionListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['view_production', 'add_production']
    queryset = Production.objects.all().order_by('id')

    def get_serializer_class(self):
        return ProductionSerializer

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

class ProductionRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['change_checklist', 'delete_checklist']
    queryset = Production.objects.all()

    def get_serializer_class(self):
        return ProductionSerializer
    
    # Overrider perform create method to set requested user
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class ProductionItemCreateAPIView(CustomListCreateMixin, generics.CreateAPIView):
    serializer_class = ProductionItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if the related Production exists
        production_id = self.kwargs['production_id']
        try:
            production = Production.objects.get(id=production_id)
        except Production.DoesNotExist:
            raise ValidationError("Production not found.")

        # Check if the Production is approved
        if production.status == 'approved' and production.approved_by is not None:
            raise ValidationError("Cannot create item for an approved production.")

        # If all checks pass, create the item and link to the production
        serializer.save(production=production)

# Generic view to delete ProductionItem
class ProductionItemDeleteAPIView(CustomRetrieveUpdateDestroyMixin, generics.DestroyAPIView):
    queryset = ProductionItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductionItemSerializer

    def perform_destroy(self, instance):
        # Check if the related Production is approved
        production_id = instance.production.id  # Get the associated production
        production = Production.objects.get(id=production_id)

        if production.status == 'approved' and production.approved_by is not None:
            return custom_resp_hand({}, status=http_status.HTTP_200_OK, message="Cannot delete item from an approved production.")

        # If all checks pass, proceed to delete the item
        instance.delete()