from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import RegistrationAPIView, LoginAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename="User")

app_name = 'authentication'
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
