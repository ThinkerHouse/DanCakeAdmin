from numpy import insert
from rest_framework import serializers
from django.db import transaction
from apps.returns.models import Returns, ReturnItem
from config.util.serializers.serializers_utils import get_created_by, get_updated_by, get_approved_by

class ReturnItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ReturnItem
        fields = ['id', 'item_id', 'quantity']
        read_only_fields = ['id']

class ReturnsSerializer(serializers.ModelSerializer):
    updated_by_info = serializers.SerializerMethodField(read_only=True)
    created_by_info = serializers.SerializerMethodField(read_only=True)
    return_items = ReturnItemSerializer(many=True)
    approved_by_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Returns
        fields = ["id","return_type", "referance_id", "return_to", "return_date", "status", "remarks", "created_by", "created_by_info", "approved_by", "approved_by_info", "updated_by", "updated_by_info", "return_items"]
        extra_kwargs = {
            'created_by' : {'read_only' : True},
            'updated_by' : {'read_only' : True}
        }

    def create(self, validated_data):
        with transaction.atomic():
            items_data = validated_data.pop('return_items')
            returns = Returns.objects.create(**validated_data)
            for item_data in items_data:
                ReturnItem.objects.create(
                    returns=returns, **item_data)
        return returns

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                instance.return_type = validated_data.get('return_type', instance.return_type)
                # instance.referance_id = validated_data.get('referance_id', instance.referance_id)
                instance.return_to = validated_data.get('return_to', instance.return_to)
                instance.return_date = validated_data.get('return_date', instance.return_date)
                instance.remarks = validated_data.get('remarks', instance.remarks)
                instance.status = validated_data.get('status', instance.status)
                instance.updated_by = validated_data.get('updated_by', instance.updated_by)
                instance.approved_by = validated_data.get('approved_by', instance.approved_by)
                instance.save()

                return_items_data = validated_data.get('return_items', [])
                existing_item_ids = [item_data.get('id') for item_data in return_items_data if item_data.get('id')]
                instance.return_items.exclude(id__in=existing_item_ids).delete()

                # Update or create purchase order items
                new_items = []
                for item_data in return_items_data:
                    item_id = item_data.get('id')
                    if item_id is not None:
                        try:
                            item = instance.return_items.get(pk=item_id)
                            item.item_id = item_data.get('item_id', item.item_id)
                            item.quantity = item_data.get('quantity', item.quantity)
                            item.save()
                        except ReturnItem.DoesNotExist:
                            pass
                    else:
                        new_items.append(ReturnItem(returns=instance, **item_data))

                ReturnItem.objects.bulk_create(new_items)
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