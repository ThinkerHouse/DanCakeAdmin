from rest_framework import serializers
from django.db import transaction
from apps.received_order.models import ReceivedOrder, ReceivedOrderItem
from config.util.serializers.serializers_utils import get_created_by, get_updated_by
from apps.material.api.serializers import MaterialSerializer
from apps.users.api.serializers import UserSerializer

# Serializes individual received order items
class ReceivedOrderItemSerializer(serializers.ModelSerializer):
    purchase_order_item_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReceivedOrderItem
        fields = ['id', 'purchase_order_item', 'purchase_order_item_info', 'quantity', 'storage_condition']

    def get_purchase_order_item_info(self, instance):
        material_data = None
        if instance.purchase_order_item.material:
            material_data = MaterialSerializer(instance.purchase_order_item.material).data
        return {
            'id': instance.purchase_order_item.id,
            'material_info': material_data,
            'quantity': instance.purchase_order_item.quantity,
            'unit_price': instance.purchase_order_item.unit_price,
            'total': instance.purchase_order_item.total,
        }

# Serializes the main received order
class ReceivedOrderSerializer(serializers.ModelSerializer):
    updated_by_info = serializers.SerializerMethodField(read_only=True)
    created_by_info = serializers.SerializerMethodField(read_only=True)
    received_order_items = ReceivedOrderItemSerializer(many=True)
    purchase_order_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReceivedOrder
        fields = [
            'id', 'batch_no', 'purchase_order', 'purchase_order_info', 'received_date', 'remarks', 'meta_data', 'status', 'created_by_info', 'created_by', 'updated_by', 'updated_by_info', 'received_order_items'
        ]
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True}
        }

    def create(self, validated_data):
        with transaction.atomic():
            items_data = validated_data.pop('received_order_items', [])
            received_order = ReceivedOrder.objects.create(**validated_data)
            for item_data in items_data:
                ReceivedOrderItem.objects.create(received_order=received_order, **item_data)
            return received_order

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                instance.purchase_order = validated_data.get('purchase_order', instance.purchase_order)
                instance.received_date = validated_data.get('received_date', instance.received_date)
                instance.remarks = validated_data.get('remarks', instance.remarks)
                instance.meta_data = validated_data.get('meta_data', instance.meta_data)
                instance.status = validated_data.get('status', instance.status)
                instance.updated_by = validated_data.get('updated_by', instance.updated_by)
                instance.save()

                items_data = validated_data.get('received_order_items', [])

                # Extract existing item IDs
                existing_item_ids = [item_data.get('id') for item_data in items_data if item_data.get('id')]
                instance.received_order_items.exclude(id__in=existing_item_ids).delete()

                # Update or create items
                new_items = []
                for item_data in items_data:
                    item_id = item_data.get('id')
                    if item_id is not None:
                        try:
                            item = instance.received_order_items.get(pk=item_id)
                            item.material = item_data.get('material', item.material)
                            item.unit = item_data.get('unit', item.unit)
                            item.quantity = item_data.get('quantity', item.quantity)
                            item.save()
                        except ReceivedOrderItem.DoesNotExist:
                            # Handle item not found
                            pass
                    else:
                        # If item has no id, create new item
                        new_items.append(ReceivedOrderItem(purchase_order=instance, **item_data))

                # Bulk create new items
                ReceivedOrderItem.objects.bulk_create(new_items)
                return instance
            except Exception as e:
                # Rollback transaction if any exception occurs
                transaction.set_rollback(True)

    def get_updated_by_info(self, instance):
        return get_updated_by(instance)

    def get_created_by_info(self, instance):
        return get_created_by(instance)
    
    def get_purchase_order_info(self, instance):
        vendor_info = None
        if hasattr(instance, 'purchase_order') and instance.purchase_order.vendor:
            # Create a dictionary of vendor information using a comprehension
            vendor_info = {
                key: UserSerializer(instance.purchase_order.vendor).data.get(key, None)
                for key in ["username", "first_name", "last_name", "email", "phone", "address"]
            }
        # Return some information about the related purchase order
        if hasattr(instance, 'purchase_order'):
            return {
                'id': instance.purchase_order.id,
                'tracking_id': instance.purchase_order.tracking_id,
                'order_date': instance.purchase_order.order_date,
                'expected_delivery_date': instance.purchase_order.expected_delivery_date,
                'delivered_at': instance.purchase_order.delivered_at,
                'total_amount': instance.purchase_order.total_amount,
                'remarks': instance.purchase_order.remarks,
                'meta_data': instance.purchase_order.meta_data,
                'status': instance.purchase_order.status,
                'vendor_info': vendor_info,
            }
        else:
            return None
