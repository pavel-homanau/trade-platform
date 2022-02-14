from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from trading import models
from trading import serializers
from trading.serializers import CreateOfferSerializer, ListOfferSerializer, ListTradeSerializer


class CurrencyViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class ItemViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


class WatchListViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer


class InventoryViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer


class OfferViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = models.Offer.objects.all()

    default_serializer_class = ListOfferSerializer
    serializer_classes = {
        'list': ListOfferSerializer,
        'retrieve': ListOfferSerializer,
        'create': CreateOfferSerializer,
    }
    http_method_names = ('get', 'post', 'patch', 'put', 'delete')

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        serializer = CreateOfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if serializer.data['order_type'] == 2:
            try:
                item_in_inventory = models.Inventory.objects. \
                    get(user=serializer.data.get('user'))
                item_in_inventory.quantity += serializer.data['entry_quantity']
                item_in_inventory.save()
            except ObjectDoesNotExist:
                item_in_inventory = models. \
                    Inventory(item=models.Item.objects.
                              get(id=serializer.data['item']),
                              user=request.current_user,
                              quantity=serializer.data['entry_quantity'])
                item_in_inventory.save()

        return Response(serializer.data)


class TradeViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,):
    queryset = models.Trade.objects.all()

    serializer_class = ListTradeSerializer
