from django.shortcuts import render, redirect, HttpResponse
from .forms import EditOrderForm
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.views import SuperuserRequiredMixin
from userprofile.models import UserProfile
from django.views.generic import View
from .models import Order
from cart.models import Cart
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.


class UpdateOrderView(SuperuserRequiredMixin, View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        form = EditOrderForm(instance=order)
        return render(
            request, "update_order.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        form = EditOrderForm(request.POST, instance=order)
        if order.status == "Completed" or order.status == "Cancelled":
            return HttpResponse("<h2>This Order have been completed or cancelled</h2>")
        elif form.is_valid():
            order.status = form.cleaned_data.get("status")
            form.save()
            return redirect("/dashboard")
        else:
            form = EditOrderForm(instance=order)
            return render(
                request, "update_order.html", {"form": form, "active": "btn-primary"}
            )


class OrdersView(LoginRequiredMixin, View):
    def get(self, request):
        op = Order.objects.filter(user=request.user)
        return render(request, "orders.html", {"order_placed": op})


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        add = UserProfile.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp_amount = p.quantity * p.product.price
                amount = int(amount) + int(temp_amount)
            total_amount = amount
        return render(
            request,
            "checkout.html",
            {"add": add, "total_amount": total_amount, "cart_items": cart_items},
        )


class PaymentDoneView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        cust_id = request.GET.get("cust_id")
        user_address = UserProfile.objects.get(id=cust_id)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            Order(
                user=user,
                user_address=user_address,
                product=c.product,
                quantity=c.quantity,
            ).save()
            c.delete()
        send_mail(
            "Order Placed Successfully",
            f"""Dear { user.username },

I am writing to inform you that your recent order has been placed successfully. We are pleased to confirm that your
order has been received and is currently being processed.

Your Order will be deliver in 30 to 40 minutes at: { user_address.address}


We would like to thank you for choosing our products and services. We are committed to delivering the highest quality
products and services to our customers, and we believe that your satisfaction is our top priority.

We will keep you updated on the progress of your order, and we will notify you once your order has been shipped. Please
note that the estimated delivery time is 30 to 40 Minutes, but this may vary depending on your location and shipping
method.

If you have any questions or concerns regarding your order, please do not hesitate to contact us. Our customer support
team is available to assist you at any time.

Thank you once again for your order, and we look forward to serving you in the future.

Best regards,

Waqas Idrees
Restaurant Name
""",
            "waqasidrees15@gmail.com",
            [f"{user.email}"],
            fail_silently=False,
        )

        send_mail(
            """You've got a New Order""",
            f"""Dear Management Team you've received an order from Customer: {user.email} kindly visit Restaurant Dashboard""",
            "waqasidrees15@gmail.com",
            [f"waqasidrees15@gmail.com"],
            fail_silently=False,
        )
        return redirect("orders")


class DashboardView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        return render(
            request, "dashboard.html", {"order": order, "active": "btn-primary"}
        )


class DeleteOrderView(SuperuserRequiredMixin, View):
    def get(self, request, pk):
        Order.objects.get(pk=pk).delete()
        return redirect("/dashboard")


class OrderSearchView(View, SuperuserRequiredMixin):
    def get(self, request):
        search = int(request.GET.get("search"))
        order = Order.objects.filter(id=search)
        return render(request, "dashboard.html", {"order": order})
    

class Api(APIView):
    def get(self, request):
        data = {"name": "waqas idrees", "age": 23}
        return Response(data)
