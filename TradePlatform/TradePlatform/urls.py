import debug_toolbar
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

SchemaView = get_schema_view(
    openapi.Info(
        title="Jaseci API",
        default_version='v1',
        description="Welcome to the world of Jaseci",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('trade/', include('trading.urls', namespace='trading')),
    path('__debug__/', include(debug_toolbar.urls)),

    path('doc/', SchemaView.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
