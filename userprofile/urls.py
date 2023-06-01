from django.urls import path
from userprofile import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "update-profile/<int:pk>",
        views.UpdateProfileView.as_view(),
        name="update-profile",
    ),
    path(
        "delete-profile/<int:pk>",
        views.DeleteProfileView.as_view(),
        name="delete-profile",
    ),
    path("address/", views.AddressView.as_view(), name="address"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
