from rest_framework import serializers

from authentication.models import User
from . import models


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


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Offer
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Inventory
        fields = '__all__'
