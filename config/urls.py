
from django.contrib import admin
from django.urls import path ,include
from drf_yasg.views import get_schema_view as get_yasg_schema_view
from drf_yasg import openapi
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),  # Include your app's URLs
]

schemma_view = get_yasg_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API endpoints",
    ),
    public=True,
)

urlpatterns += [
    path('swagger/', schemma_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schemma_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
from drf_yasg.views import get_schema_view as get_yasg_schema_view
from drf_yasg import openapi
from rest_framework.schemas import get_schema_view
from django.urls import path, include