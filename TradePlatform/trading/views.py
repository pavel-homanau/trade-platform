from abc import abstractmethod

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from trading import models
from trading import serializers


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


class TestView(APIView):

    def get(self, request):
        return Response({"msg": "main test ok"})
