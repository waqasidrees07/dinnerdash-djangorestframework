from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.ProductView.as_view(), name="home"),
    path(
        "product-detail/<int:pk>",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
    path("burger/", views.BurgerView.as_view(), name="burger"),
    path("pizza/", views.PizzaView.as_view(), name="pizza"),
    path("sandwich/", views.SandwichView.as_view(), name="sandwich"),
    path("shakes/", views.ShakesView.as_view(), name="shakes"),
    path("fries/", views.FriesView.as_view(), name="fries"),
    path(
        "update-product/<int:pk>",
        views.UpdateProductView.as_view(),
        name="update-product",
    ),
    path(
        "delete-product/<int:pk>",
        views.DeleteProductView.as_view(),
        name="delete-product",
    ),
    path("add-product/", views.AddProductView.as_view(), name="add-product"),
    path("products/", views.ProductsView.as_view(), name="products"),
    path("search-products/", views.ProductSearchView.as_view(), name="search-products"),
    path("add-category/", views.AddCategoryView.as_view(), name="add-category"),
    path("categories/", views.CategoryView.as_view(), name="category"),
    path("add-restaurant/", views.AddRestaurantView.as_view(), name="add-restaurant"),
    path("restaurants/", views.RestaurantsView.as_view(), name="restaurants"),
    path("dha-branch/", views.DHABranchView.as_view(), name="dha-branch"),
    path("gulberg-branch/", views.GulbergBranchView.as_view(), name="gulberg-branch"),
    path(
        "update-restaurants/<int:pk>",
        views.UpdateRestaurantView.as_view(),
        name="update-restaurants",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
