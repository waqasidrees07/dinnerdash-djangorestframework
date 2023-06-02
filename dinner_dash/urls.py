from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("", include("product.urls")),
    path("", include("cart.urls")),
    path("", include("userprofile.urls")),
    path("", include("order.urls")),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
