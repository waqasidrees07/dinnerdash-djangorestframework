from django.shortcuts import render, redirect
from .models import Product, Category, Restaurant
from django.views.generic import View
from .forms import AddProductForm, AddCategoryForm, AddRestaurantForm
from django.contrib import messages
from authentication.views import SuperuserRequiredMixin
from rest_framework.views import Response, APIView
from .serializer import AddRestaurantSerializer, GetRestaurantSerializer, GetProductSerializer, AddProductSerializer
from rest_framework import status


# Create your views here.


class ProductView(APIView):
    def get(self, request):
        burger = Product.objects.filter(category__category__contains="Burger")
        pizza = Product.objects.filter(category__category__contains="Pizza")
        sandwich = Product.objects.filter(category__category__contains="Sandwich")
        shakes = Product.objects.filter(category__category__contains="Shakes")

        burger_serializer = GetProductSerializer(burger)
        pizza_serializer = GetProductSerializer(pizza)
        sandwich_serializer = GetProductSerializer(sandwich)
        shakes_serializer = GetProductSerializer(shakes)
        context = {
            "burger": burger_serializer.data,
            "pizza": pizza_serializer.data,
            "sandwich": sandwich_serializer.data,
            "shakes": shakes_serializer.data,

        }
        return Response({"products": context})


class BurgerView(View):
    def get(self, request):
        burger = Product.objects.filter(category__category__contains="Burger")
        return render(request, "burger.html", {"burger": burger})


class PizzaView(View):
    def get(self, request):
        pizza = Product.objects.filter(category__category__contains="Pizza")
        return render(request, "pizza.html", {"pizza": pizza})


class SandwichView(View):
    def get(self, request):
        sandwich = Product.objects.filter(category__category__contains="Sandwich")
        return render(request, "sandwich.html", {"sandwich": sandwich})


class ShakesView(View):
    def get(self, request):
        shakes = Product.objects.filter(category__category__contains="Shakes")
        return render(request, "shakes.html", {"shakes": shakes})


class FriesView(View):
    def get(self, request):
        fries = Product.objects.filter(category__category__contains="Fries")
        return render(request, "fries.html", {"fries": fries})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "product_detail.html", {"Product": product})


class AddProductView(APIView):
    serializer_class = AddProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Product Added Successfully", "product": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateProductView(SuperuserRequiredMixin, View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = AddProductForm(instance=product)
        return render(
            request, "add_product.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request, pk, **kwargs):
        product = Product.objects.get(pk=pk)
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product.title = form.cleaned_data["title"]
            product.description = form.cleaned_data["description"]
            product.price = form.cleaned_data["price"]
            product.category = form.cleaned_data["category"]
            product.image = form.cleaned_data["image"]
            product.restaurant = form.cleaned_data["restaurant"]
            form.save()
            messages.success(
                request, "Congratulations!! Product Updated successfully..."
            )
        else:
            form = AddProductForm()
        return render(
            request, "add_product.html", {"form": form, "active": "btn-primary"}
        )


class DeleteProductView(SuperuserRequiredMixin, View):
    def get(self, request, pk):
        Product.objects.get(pk=pk).delete()
        return redirect("/products")


class ProductsView(SuperuserRequiredMixin, View):
    def get(self, request):
        product = Product.objects.all()
        return render(
            request,
            "products.html",
            {"product": product, "active": "btn-primary"},
        )


class AddCategoryView(SuperuserRequiredMixin, View):
    def get(self, request):
        form = AddCategoryForm()
        return render(
            request, "add_category.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request):
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            reg = Category(category=category)
            reg.save()
            messages.success(request, "Congratulation!! Category Added Successfully")
        else:
            form = AddCategoryForm
        return render(
            request, "add_category.html", {"form": form, "active": "btn-primary"}
        )


class CategoryView(SuperuserRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(
            request,
            "category.html",
            {"categories": categories, "active": "btn-primary"},
        )


class AddRestaurantView(APIView):
    serializer_class = AddRestaurantSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Restaurant Added successfully', "restaurant": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRestaurantView(APIView):

    def post(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        form = AddRestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            restaurant.title = form.cleaned_data["title"]
            restaurant.address = form.cleaned_data["address"]
            restaurant.city = form.cleaned_data["city"]
            form.save()
            messages.success(
                request, "Congratulation!! Restaurant Updated Successfully"
            )
            return redirect("/restaurants")
        else:
            form = AddRestaurantForm
        return render(
            request,
            "add_restaurant.html",
            {"form": form, "active": "btn-primary"},
        )


class RestaurantsView(APIView):  # Need SuperuserLogin
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = GetRestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


class DHABranchView(View):
    def get(self, request):
        products = Product.objects.filter(restaurant__title__contains="DHA Branch")
        return render(request, "dha_branch.html", {"products": products})


class GulbergBranchView(View):
    def get(self, request):
        products = Product.objects.filter(restaurant__title__contains="Gulberg Branch")
        return render(request, "dha_branch.html", {"products": products})


class ProductSearchView(View, SuperuserRequiredMixin):
    def get(self, request):
        search = request.GET.get("search")
        product = Product.objects.filter(title__contains=search)
        return render(request, "products.html", {"product": product})
