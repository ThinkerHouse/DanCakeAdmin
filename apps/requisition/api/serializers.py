from numpy import insert
from rest_framework import serializers
from django.db import transaction
from apps import requisition
from apps.requisition.models import Requisition, RequisitionItem
from config.util.serializers.serializers_utils import get_created_by, get_updated_by

class RequisitionItemSerializer(serializers.ModelSerializer):
    material_info = serializers.SerializerMethodField(read_only=True)
    # unit_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RequisitionItem
        # fields = ['id','unit', 'unit_info', 'material', 'material_info', 'quantity']
        fields = ['id', 'material', 'material_info', 'quantity']

    # def get_unit_info(self, instance):
    #     return {
    #         'id': instance.unit.id,
    #         'name': instance.unit.name,
    #     }
    
    def get_material_info(self, instance):
        return {
            'id': instance.material.id,
            'name': instance.material.name,
            'unit': instance.material.unit.name,
            'unit_shortname': instance.material.unit.short_name,
        }

class RequisitionSerializer(serializers.ModelSerializer):
    updated_by_info = serializers.SerializerMethodField(read_only=True)
    created_by_info = serializers.SerializerMethodField(read_only=True)
    requisition_items = RequisitionItemSerializer(many=True)
    department_info = serializers.SerializerMethodField(read_only=True)
    production_info = serializers.SerializerMethodField(read_only=True)
    approved_by_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Requisition
        fields = ["id", "batch_no", "department", "department_info", "production", "production_info", "date_requested", "expected_delivery_date", "delivered_at", "remarks", "purpose", "status", "meta_data", "created_by", "created_by_info", "approved_by", "approved_by_info", "updated_by", "updated_by_info", "requisition_items"]
        extra_kwargs = {
            'created_by' : {'read_only' : True},
            'updated_by' : {'read_only' : True}
        }

    def create(self, validated_data):
        with transaction.atomic():
            items_data = validated_data.pop('requisition_items')
            requisition = Requisition.objects.create(**validated_data)
            for item_data in items_data:
                RequisitionItem.objects.create(
                    requisition=requisition, **item_data)
        return requisition

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                instance.department = validated_data.get('department', instance.department)
                instance.expected_delivery_date = validated_data.get('expected_delivery_date', instance.expected_delivery_date)
                instance.delivered_at = validated_data.get('delivered_at', instance.delivered_at)
                instance.remarks = validated_data.get('remarks', instance.remarks)
                instance.purpose = validated_data.get('purpose', instance.purpose)
                instance.meta_data = validated_data.get('meta_data', instance.meta_data)
                instance.status = validated_data.get('status', instance.status)
                instance.updated_by = validated_data.get('updated_by', instance.updated_by)
                instance.approved_by = validated_data.get('approved_by', instance.approved_by)
                instance.save()

                items_data = validated_data.get('requisition_items', [])

                # Extract existing item IDs
                existing_item_ids = [item_data.get('id') for item_data in items_data if item_data.get('id')]

                instance.requisition_items.exclude(id__in=existing_item_ids).delete()

                # Update or create items
                new_items = []
                for item_data in items_data:
                    item_id = item_data.get('id')
                    if item_id is not None:
                        try:
                            item = instance.requisition_items.get(pk=item_id)
                            item.material = item_data.get('material', item.material)
                            # item.unit = item_data.get('unit', item.unit)
                            item.quantity = item_data.get('quantity', item.quantity)
                            item.save()
                        except RequisitionItem.DoesNotExist:
                            # Handle item not found
                            pass
                    else:
                        # If item has no id, create new item
                        new_items.append(RequisitionItem(requisition=instance, **item_data))

                # Bulk create new items
                RequisitionItem.objects.bulk_create(new_items)
                return instance

            except Exception as e:
                # Rollback transaction if any exception occurs
                transaction.set_rollback(True)

    def get_updated_by_info(self, instance):
        return get_updated_by(instance)

    def get_created_by_info(self, instance):
        return get_created_by(instance)
    
    def get_department_info(self, instance):
        return {
            'id': instance.department.id,
            'name': instance.department.name
        }
    
    def get_production_info(self, instance):
        return {
            'id': instance.production.id,
            'name': instance.production.name
        }
    
    def get_approved_by_info(self, instance):
        if instance.approved_by:
            return {
                'id': instance.approved_by.id,
                'name': instance.approved_by.username,
            }
        return None
