from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trading.views import ( CurrencyViewSet, ItemViewSet,
                            WatchListViewSet, OfferViewSet,
                            InventoryViewSet)

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet, basename="Currency")
router.register(r'items', ItemViewSet, basename="Item")
router.register(r'watchlists', WatchListViewSet, basename="WatchList")
router.register(r'offers', OfferViewSet, basename="Offer")
router.register(r'inventories', InventoryViewSet, basename="Inventory")

app_name = 'trading'
urlpatterns = [
    path('', include(router.urls)),
]
