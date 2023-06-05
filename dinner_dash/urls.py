from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Your API description",
    ),
    public=True,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("", include("product.urls")),
    path("", include("cart.urls")),
    path("", include("userprofile.urls")),
    path("", include("order.urls")),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api_docs'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
