from django.urls import include, path
from rest_framework.routers import DefaultRouter

from authentication import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename="User")
router.register(r'auth', views.AuthorizationViewSet, basename='Auth')

app_name = 'authentication'
urlpatterns = [
    path('', include(router.urls)),
]
