from abc import abstractmethod

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, status
from rest_framework.response import Response

from authentication.models import User
from trading import models
from trading import serializers


class DefaultViewSet(viewsets.ViewSet):
    @property
    @abstractmethod
    def queryset(self):
        pass

    @property
    @abstractmethod
    def serializer_class(self):
        pass

    class Meta:
        abstract = True

    @method_decorator(cache_page(5 * 60))
    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.filter(id=kwargs.get('pk'))
        instance.delete()

        return Response(status.HTTP_204_NO_CONTENT)


class CurrencyViewSet(DefaultViewSet):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class ItemViewSet(DefaultViewSet):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


class WatchListViewSet(DefaultViewSet):
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer


class InventoryViewSet(DefaultViewSet):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer


class OfferViewSet(DefaultViewSet):
    queryset = models.Offer.objects.all()
    serializer_class = serializers.OfferSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if serializer.data['order_type'] == 2:
            try:
                current_user = User.objects.get(id=serializer.data['user'])
                item_in_inventory = models.Inventory.objects. \
                    get(user=current_user)
                item_in_inventory.quantity += serializer.data['entry_quantity']
                item_in_inventory.save()
            except ObjectDoesNotExist:
                item_in_inventory = models. \
                    Inventory(item=models.Item.objects.
                              get(id=serializer.data['item']),
                              user=current_user,
                              quantity=serializer.data['entry_quantity'])
                item_in_inventory.save()

        return Response(serializer.data)
