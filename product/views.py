from django.shortcuts import render, redirect
from .models import Product, Category, Restaurant
from django.views.generic import View
from .forms import AddProductForm, AddCategoryForm, AddRestaurantForm
from django.contrib import messages
from authentication.views import SuperuserRequiredMixin

# Create your views here.


class ProductView(View):
    def get(self, request):
        burger = Product.objects.filter(category__category__contains="Burger")
        pizza = Product.objects.filter(category__category__contains="Pizza")
        sandwich = Product.objects.filter(category__category__contains="Sandwich")
        shakes = Product.objects.filter(category__category__contains="Shakes")
        context = {
            "burger": burger,
            "pizza": pizza,
            "sandwich": sandwich,
            "shakes": shakes,
        }
        return render(request, "home.html", context)


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


class AddProductView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = AddProductForm()
        return render(
            request, "add_product.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request, *args, **kwargs):
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]
            restaurant = form.cleaned_data["restaurant"]
            reg, created = Product.objects.get_or_create(
                title=title,
                description=description,
                price=price,
                image=image,
                category=category,
                restaurant=restaurant,
            )
            reg.save()
            messages.success(request, "Congratulations!! Product Added Successfully...")
            return redirect("/add-product")
        else:
            form = AddProductForm()
            messages.error(request, "Price must be greater than 0")
        return render(
            request, "add_product.html", {"form": form, "active": "btn-primary"}
        )


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


class AddRestaurantView(SuperuserRequiredMixin, View):
    def get(self, request):
        form = AddRestaurantForm()
        return render(
            request,
            "add_restaurant.html",
            {"form": form, "active": "btn-primary"},
        )

    def post(self, request):
        form = AddRestaurantForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            address = form.cleaned_data["address"]
            city = form.cleaned_data["city"]
            reg = Restaurant(title=title, address=address, city=city)
            reg.save()
            messages.success(request, "Congratulation!! Restaurant Added Successfully")
        else:
            form = AddRestaurantForm
        return render(
            request,
            "add_restaurant.html",
            {"form": form, "active": "btn-primary"},
        )


class UpdateRestaurantView(SuperuserRequiredMixin, View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        form = AddRestaurantForm(instance=restaurant)
        return render(
            request,
            "add_restaurant.html",
            {"form": form, "active": "btn-primary"},
        )

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


class RestaurantsView(SuperuserRequiredMixin, View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        return render(
            request,
            "restaurants.html",
            {"restaurants": restaurants, "active": "btn-primary"},
        )


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
