from django.urls import include, path
from rest_framework.routers import DefaultRouter

from trading import views

router = DefaultRouter()
router.register(r'currencies', views.CurrencyViewSet, basename="Currency")
router.register(r'items', views.ItemViewSet, basename="Item")
router.register(r'watchlists', views.WatchListViewSet, basename="WatchList")
router.register(r'offers', views.OfferViewSet, basename="Offer")
router.register(r'inventories', views.InventoryViewSet, basename="Inventory")

app_name = 'trading'
urlpatterns = [
    path('', include(router.urls)),
    # path('aa-test/', TestView.as_view())
]
