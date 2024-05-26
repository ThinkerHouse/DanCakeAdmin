from numpy import insert
from rest_framework import serializers
from django.db import transaction
from apps.production.models import Production, ProductionItem
from config.util.serializers.serializers_utils import get_created_by, get_updated_by, get_approved_by, get_production_plant, get_product, get_unit

class ProductionItemSerializer(serializers.ModelSerializer):
    product_info = serializers.SerializerMethodField(read_only=True)
    # unit_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductionItem
        fields = ['id', 'product', 'product_info', 'quantity']

    # def get_unit_info(self, instance):
    #     return get_unit(instance)
    
    def get_product_info(self, instance):
        return get_product(instance)

class ProductionSerializer(serializers.ModelSerializer):
    updated_by_info = serializers.SerializerMethodField(read_only=True)
    created_by_info = serializers.SerializerMethodField(read_only=True)
    production_items = ProductionItemSerializer(many=True)
    production_plant_info = serializers.SerializerMethodField(read_only=True)
    approved_by_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Production
        fields = ["id", "name", "batch_no", "production_plant", "production_plant_info", "expected_delivery_date", "delivered_at", "remarks", "status", "meta_data", "created_by", "created_by_info", "approved_by", "approved_by_info", "updated_by", "updated_by_info", "production_items"]
        extra_kwargs = {
            'created_by' : {'read_only' : True},
            'updated_by' : {'read_only' : True}
        }

    def create(self, validated_data):
        with transaction.atomic():
            items_data = validated_data.pop('production_items')
            production = Production.objects.create(**validated_data)
            for item_data in items_data:
                ProductionItem.objects.create(
                    production=production, **item_data)
        return production

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                instance.name = validated_data.get('name', instance.name)
                instance.production_plant = validated_data.get('production_plant', instance.production_plant)
                instance.expected_delivery_date = validated_data.get('expected_delivery_date', instance.expected_delivery_date)
                instance.delivered_at = validated_data.get('delivered_at', instance.delivered_at)
                instance.remarks = validated_data.get('remarks', instance.remarks)
                instance.meta_data = validated_data.get('meta_data', instance.meta_data)
                instance.status = validated_data.get('status', instance.status)
                instance.updated_by = validated_data.get('updated_by', instance.updated_by)
                instance.approved_by = validated_data.get('approved_by', instance.approved_by)
                instance.save()

                items_data = validated_data.get('production_items', [])

                # Extract existing item IDs
                existing_item_ids = [item_data.get('id') for item_data in items_data if item_data.get('id')]
                instance.production_items.exclude(id__in=existing_item_ids).delete()

                # Update or create items
                new_items = []
                for item_data in items_data:
                    item_id = item_data.get('id')
                    if item_id is not None:
                        try:
                            item = instance.production_items.get(pk=item_id)
                            item.material = item_data.get('material', item.material)
                            # item.unit = item_data.get('unit', item.unit)
                            item.quantity = item_data.get('quantity', item.quantity)
                            item.save()
                        except ProductionItem.DoesNotExist:
                            # Handle item not found
                            pass
                    else:
                        # If item has no id, create new item
                        new_items.append(ProductionItem(production=instance, **item_data))

                # Bulk create new items
                ProductionItem.objects.bulk_create(new_items)
                return instance
            except Exception as e:
                # Rollback transaction if any exception occurs
                transaction.set_rollback(True)

    def get_production_plant_info(self, instance):
        return get_production_plant(instance)

    def get_updated_by_info(self, instance):
        return get_updated_by(instance)

    def get_created_by_info(self, instance):
        return get_created_by(instance)
    
    def get_approved_by_info(self, instance):
        return get_approved_by(instance)