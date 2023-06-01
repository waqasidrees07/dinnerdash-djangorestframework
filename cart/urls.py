from django.urls import path
from cart import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("add-to-cart/", views.AddToCartView.as_view(), name="add-to-cart"),
    path("cart/", views.ShowCartView.as_view(), name="showcart"),
    path("pluscart/", views.PlusCartView.as_view(), name="pluscart"),
    path("minuscart/", views.MinusCartView.as_view(), name="minuscart"),
    path("removecart/", views.RemoveCartView.as_view(), name="removecart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
