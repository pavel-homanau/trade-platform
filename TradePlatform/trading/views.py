from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from . import models
from . import serializers
from .tasks import tst_task


class DefaultViewSet(viewsets.ViewSet):
    class Meta:
        abstract = True

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
                item_in_inventory = models.Inventory.objects.get(user=User.objects.get(id=serializer.data['user']))
                item_in_inventory.quantity += serializer.data['entry_quantity']
                item_in_inventory.save()
            except ObjectDoesNotExist:
                item_in_inventory = models.Inventory(item=models.Item.objects.get(id=serializer.data['item']),
                                                     user=User.objects.get(id=serializer.data['user']),
                                                     quantity=serializer.data['entry_quantity'])
                item_in_inventory.save()

        return Response(serializer.data)


class tst(APIView):
    def get(self, request):
        tst = 0
        print(datetime.now())
        if tst == 1:
            active_offers = models.Offer.objects.filter(is_active=True)
            buy_offers = active_offers.filter(order_type=1)
            sell_offers = active_offers.filter(order_type=2)
            for buy_offer in buy_offers:
                filtered_sell_offers = sell_offers.filter(item=buy_offer.item,
                                                          entry_quantity__gte=buy_offer.entry_quantity,
                                                          price__gte=buy_offer.price)
                if filtered_sell_offers:
                    sell_offer = filtered_sell_offers.order_by('price', 'entry_quantity').first()
                    seller = User.objects.get(email=sell_offer.user)
                    buyer = User.objects.get(email=buy_offer.user)
                    trade_object = models.Trade(item=buy_offer.item,
                                                buyer=buyer,
                                                seller=seller,
                                                quantity=buy_offer.entry_quantity,
                                                unit_price=sell_offer.price,
                                                buyer_offer=buy_offer,
                                                seller_offer=sell_offer)

                    if (buyer.cash - trade_object.unit_price * trade_object.quantity) >= 0:
                        # process with cash
                        seller.cash += trade_object.unit_price * trade_object.quantity
                        seller.save()

                        buyer.cash -= trade_object.unit_price * trade_object.quantity
                        buyer.save()

                        # process with inventory
                        item_in_buyer_inventory = models.Inventory.objects.filter(user=buyer)
                        item_in_seller_inventory = models.Inventory.objects.get(user=seller)
                        if item_in_buyer_inventory:
                            item_in_buyer_inventory = item_in_buyer_inventory[0]
                            item_in_buyer_inventory.quantity += trade_object.quantity
                        else:
                            item_in_buyer_inventory = models.Inventory(item=buy_offer.item,
                                                                       user=buyer,
                                                                       quantity=trade_object.quantity)
                        item_in_buyer_inventory.save()
                        item_in_seller_inventory.quantity -= trade_object.quantity
                        item_in_seller_inventory.save()

                        # delete if item is empty
                        if item_in_seller_inventory.quantity == 0:
                            item_in_seller_inventory.delete()

                        trade_object.save()

                        buy_offer.is_active = False
                        buy_offer.save()

                        if sell_offer.entry_quantity == 0:
                            sell_offer.is_active = False
                            sell_offer.save()
        return Response()
