from rest_framework import serializers

from trading import models
from trading.models import Offer


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Currency
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Item
        fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WatchList
        fields = '__all__'


class ListOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = '__all__'


class CreateOfferSerializer(serializers.ModelSerializer):
    current_quantity = serializers.StringRelatedField(source='entry_quantity')

    def create(self, validated_data):
        validated_data['current_quantity'] = validated_data.get('entry_quantity')
        return super().create(validated_data)

    class Meta:
        model = models.Offer
        fields = ('order_type', 'user', 'item', 'entry_quantity', 'price', 'current_quantity')


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Inventory
        fields = '__all__'
