from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework.response import Response

from trading.models import (Currency, Item, WatchList,
                            Inventory, Offer)
from trading.services import CheckPrice
from trading.serializers import (CurrencySerializer, ItemSerializer,
                                 WatchListSerializer, InventorySerializer,
                                 OfferSerializer)

CACHE_TIMEOUT = 5 * 60


@method_decorator(name='list', decorator=cache_page(CACHE_TIMEOUT))
class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


@method_decorator(name='list', decorator=cache_page(CACHE_TIMEOUT))
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


@method_decorator(name='list', decorator=cache_page(CACHE_TIMEOUT))
class WatchListViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


@method_decorator(name='list', decorator=cache_page(CACHE_TIMEOUT))
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


@method_decorator(name='list', decorator=cache_page(CACHE_TIMEOUT))
class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if serializer.data['order_type'] == 2:
            CheckPrice.execute({
                'serializer': serializer.data
            })

        return Response(serializer.data)
