# import debug_toolbar
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Test API",
      default_version='v1',
   ),
)

urlpatterns = [
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('api/', include('trading.urls', namespace='trading')),
    # path('__debug__/', include(debug_toolbar.urls)),
    path(r'docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]
