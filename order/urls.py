from django.urls import path
from order import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("orders/", views.OrdersView.as_view(), name="orders"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("paymentdone/", views.PaymentDoneView.as_view(), name="paymentdone"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("update-order/<int:pk>", views.UpdateOrderView.as_view(), name="updateorder"),
    path("delete-order/<int:pk>", views.DeleteOrderView.as_view(), name="deleteorder"),
    path("order-search", views.OrderSearchView.as_view(), name="search-order"),
    path("firstapi/", views.Api.as_view())
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
