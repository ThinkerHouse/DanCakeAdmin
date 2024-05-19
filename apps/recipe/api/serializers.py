from numpy import insert
from rest_framework import serializers
from django.db import transaction
from apps import recipe
from apps.recipe.models import Recipe, RecipeItem
from config.util.serializers.serializers_utils import get_created_by, get_updated_by, get_approved_by

class RecipeItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    material_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RecipeItem
        fields = ['id', 'material', 'material_info', 'quantity', 'status']
        read_only_fields = ['id']
    
    def get_material_info(self, instance):
        return {
            'id': instance.material.id,
            'name': instance.material.name,
        }

class RecipeSerializer(serializers.ModelSerializer):
    updated_by_info = serializers.SerializerMethodField(read_only=True)
    created_by_info = serializers.SerializerMethodField(read_only=True)
    recipe_items = RecipeItemSerializer(many=True)
    product_info = serializers.SerializerMethodField(read_only=True)
    approved_by_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ["id","name", "product", "product_info", "status", "created_by", "created_by_info", "approved_by", "approved_by_info", "updated_by", "updated_by_info", "recipe_items"]
        extra_kwargs = {
            'created_by' : {'read_only' : True},
            'updated_by' : {'read_only' : True}
        }

    def create(self, validated_data):
        with transaction.atomic():
            items_data = validated_data.pop('recipe_items')
            recipe = Recipe.objects.create(**validated_data)
            for item_data in items_data:
                RecipeItem.objects.create(
                    recipe=recipe, **item_data)
        return recipe

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                instance.name = validated_data.get('name', instance.name)
                instance.product = validated_data.get('product', instance.product)
                instance.status = validated_data.get('status', instance.status)
                instance.updated_by = validated_data.get('updated_by', instance.updated_by)
                instance.approved_by = validated_data.get('approved_by', instance.approved_by)
                instance.save()

                # Retrieve recipe_items_data
                recipe_items_data = validated_data.get('recipe_items', [])

                # Extract existing item IDs
                existing_item_ids = [item_data.get('id') for item_data in recipe_items_data if item_data.get('id')]

                # Delete purchase order items not included in recipe_items_data
                instance.recipe_items.exclude(id__in=existing_item_ids).delete()

                # Update or create purchase order items
                new_items = []
                for item_data in recipe_items_data:
                    item_id = item_data.get('id')
                    if item_id is not None:
                        try:
                            item = instance.recipe_items.get(pk=item_id)
                            item.material = item_data.get('material', item.material)
                            item.quantity = item_data.get('quantity', item.quantity)
                            item.status = item_data.get('status', item.status)
                            item.save()
                        except RecipeItem.DoesNotExist:
                            pass
                    else:
                        new_items.append(RecipeItem(recipe=instance, **item_data))

                RecipeItem.objects.bulk_create(new_items)
                return instance
            except Exception as e:
                transaction.set_rollback(True)
                raise e

    def get_updated_by_info(self, instance):
        return get_updated_by(instance)

    def get_created_by_info(self, instance):
        return get_created_by(instance)
    
    def get_approved_by_info(self, instance):
        return get_approved_by(instance=instance)
    
    def get_product_info(self, instance):
        return {
            'id': instance.product.id,
            'name': instance.product.name
        }