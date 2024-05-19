from numpy import insert
from rest_framework import serializers
from django.db import transaction

from apps.purchase_order.models import PurchaseOrder, PurchaseOrderItem
from config.util.serializers.serializers_utils import get_created_by, get_updated_by


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    material_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'material', 'material_info',
                  'quantity', 'unit_price', 'total']
        read_only_fields = ['id']

    def get_material_info(self, instance):
        return {
            'id': instance.material.id,
            'name': instance.material.name,
        }


class PurchaseOrderSerializer(serializers.ModelSerializer):
    updated_by_info = serializers.SerializerMethodField(read_only=True)
    created_by_info = serializers.SerializerMethodField(read_only=True)
    purchase_order_items = PurchaseOrderItemSerializer(many=True)
    vendor_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ["id", "tracking_id", "vendor", "order_date", "updated_by", "created_by", "vendor_info", "updated_by_info", "created_by_info",
                  "expected_delivery_date", "delivered_at", "total_amount", "remarks", "meta_data", "status", "purchase_order_items"]
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True}
        }

    def create(self, validated_data):
        try:
            with transaction.atomic():
                items_data = validated_data.pop('purchase_order_items')
                purchase_order = PurchaseOrder.objects.create(**validated_data)
                for item_data in items_data:
                    PurchaseOrderItem.objects.create(
                        purchase_order=purchase_order, **item_data)
            return purchase_order
        except Exception as e:
            transaction.set_rollback(True)

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                # Update purchase order fields
                instance.tracking_id = validated_data.get('tracking_id', instance.tracking_id)
                instance.vendor = validated_data.get('vendor', instance.vendor)
                instance.order_date = validated_data.get('order_date', instance.order_date)
                instance.expected_delivery_date = validated_data.get('expected_delivery_date', instance.expected_delivery_date)
                instance.delivered_at = validated_data.get('delivered_at', instance.delivered_at)
                instance.total_amount = validated_data.get('total_amount', instance.total_amount)
                instance.remarks = validated_data.get('remarks', instance.remarks)
                instance.meta_data = validated_data.get('meta_data', instance.meta_data)
                instance.status = validated_data.get('status', instance.status)
                instance.updated_by = validated_data.get('updated_by', instance.updated_by)
                instance.save()

                # Retrieve purchase_order_items_data
                purchase_order_items_data = validated_data.get('purchase_order_items', [])

                # Extract existing item IDs
                existing_item_ids = [item_data.get('id') for item_data in purchase_order_items_data if item_data.get('id')]
                
                # Delete purchase order items not included in purchase_order_items_data
                instance.purchase_order_items.exclude(id__in=existing_item_ids).delete()

                # Update or create purchase order items
                new_items = []
                for item_data in purchase_order_items_data:
                    item_id = item_data.get('id')
                    if item_id is not None:
                        try:
                            item = instance.purchase_order_items.get(pk=item_id)
                            item.material = item_data.get('material', item.material)
                            item.quantity = item_data.get('quantity', item.quantity)
                            item.unit_price = item_data.get('unit_price', item.unit_price)
                            item.total = item_data.get('total', item.total)
                            item.save()
                        except PurchaseOrderItem.DoesNotExist:
                            # Handle item not found
                            pass
                    else:
                        # If item has no id, create new item
                        new_items.append(PurchaseOrderItem(purchase_order=instance, **item_data))

                # Bulk create new items
                PurchaseOrderItem.objects.bulk_create(new_items)

                return instance

            except Exception as e:
                # Rollback transaction if any exception occurs
                transaction.set_rollback(True)

    def get_updated_by_info(self, instance):
        return get_updated_by(instance)

    def get_created_by_info(self, instance):
        return get_created_by(instance)

    def get_vendor_info(self, instance):
        return {
            'id': instance.vendor.id,
            'username': instance.vendor.username
        }
