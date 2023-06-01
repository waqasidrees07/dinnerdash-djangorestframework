from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Cart
# Create your views here.


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        product_id = self.request.GET.get("prod_id")
        cart = Cart.objects.filter(user=user, product_id=product_id).first()
        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart(user=user, product_id=product_id).save()
        return redirect("/cart")


class ShowCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    tempamount = p.quantity * p.product.price
                    amount = int(amount) + int(tempamount)
                    total_amount = amount
                    context = {
                        "carts": cart,
                        "totalamount": total_amount,
                        "amount": amount,
                    }
                return render(request, "add_to_cart.html", context)
            else:
                return render(request, "empty_cart.html")


class PlusCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            prod_id = request.GET["prod_id"]
            c = Cart.objects.get(product=prod_id, user=request.user)
            c.quantity += 1
            c.save()
            amount = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount = p.quantity * p.product.price
                amount = int(amount) + int(tempamount)
            data = {
                "quantity": c.quantity,
                "totalamount": amount,
            }
            return JsonResponse(data)


class MinusCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            prod_id = request.GET["prod_id"]
            c = Cart.objects.get(product=prod_id, user=request.user)
            c.quantity -= 1
            c.save()

            if c.quantity == 0:
                c.delete()
                quantity = 0
                amount = 0

            else:
                quantity = c.quantity
                amount = 0.0
                cart_product = [p for p in Cart.objects.all() if p.user == request.user]
                for p in cart_product:
                    tempamount = p.quantity * p.product.price
                    amount = int(amount) - int(tempamount)
            if quantity == 0:
                return redirect("/cart")

            data = {
                "quantity": quantity,
                "totalamount": amount,
            }
            return JsonResponse(data)


class RemoveCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            prod_id = request.GET["prod_id"]
            c = Cart.objects.get(product=prod_id, user=request.user)
            c.delete()
            amount = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount = p.quantity * p.product.price
                amount = int(amount) + int(tempamount)
            data = {
                "quantity": c.quantity,
                "totalamount": amount,
            }
            return JsonResponse(data)
