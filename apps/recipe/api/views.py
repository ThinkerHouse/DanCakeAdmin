from rest_framework import generics, status as http_status
from rest_framework.exceptions import ValidationError
from config.util.mixins.BasicCustomMixin import CustomListCreateMixin, CustomRetrieveUpdateDestroyMixin
from config.util.mixins.QueryParamsFilterMixin import BasicQueryParamsFilterMixin
from rest_framework.permissions import IsAuthenticated
from config.util.permissions.GroupPermission import GroupPermission
from apps.recipe.api.serializers import RecipeSerializer, RecipeItemSerializer
from apps.recipe.models import Recipe, RecipeItem
from config.util.response_handler.custom_response_handler import custom_response_handler as custom_resp_hand

class RecipeListCreateAPIView(BasicQueryParamsFilterMixin, CustomListCreateMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['view_production', 'add_production']
    queryset = Recipe.objects.all().order_by('id')

    def get_serializer_class(self):
        return RecipeSerializer

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

class RecipeRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, GroupPermission]
    # required_permissions = ['change_checklist', 'delete_checklist']
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        return RecipeSerializer
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class RecipeItemCreateAPIView(CustomListCreateMixin, generics.CreateAPIView):
    serializer_class = RecipeItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        recipe_id = self.kwargs['recipe_id']
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise ValidationError("Recipe not found.")

        if recipe.status == 'approved' and recipe.approved_by is not None:
            raise ValidationError("Cannot create item for an approved recipe.")

        serializer.save(recipe=recipe)

# Generic view to delete RecipeItem
class RecipeItemDeleteAPIView(CustomRetrieveUpdateDestroyMixin, generics.DestroyAPIView):
    queryset = RecipeItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeItemSerializer

    def perform_destroy(self, instance):
        recipe_id = instance.recipe.id
        recipe = Recipe.objects.get(id=recipe_id)
        if recipe.status == 'approved' and recipe.approved_by is not None:
            return custom_resp_hand({}, status=http_status.HTTP_200_OK, message="Cannot delete item from an approved requisition.")
        instance.delete()