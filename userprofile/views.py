from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages

# Create your views here.


class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        add = UserProfile.objects.filter(user=request.user)
        return render(request, "address.html", {"add": add, "active": "btn-primary"})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserProfileForm()
        return render(request, "profile.html", {"form": form, "active": "btn-primary"})

    def post(self, request):
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            full_name = form.cleaned_data["full_name"]
            nick_name = form.cleaned_data["nick_name"]
            address = form.cleaned_data["address"]
            contact = form.cleaned_data["contact"]
            reg = UserProfile(
                user=user,
                full_name=full_name,
                nick_name=nick_name,
                address=address,
                contact=contact,
            )
            reg.save()
            messages.success(
                request,
                "Congratulations!! Address Added successfully... go to saved addresses",
            )
        return render(request, "profile.html", {"form": form, "active": "btn-primary"})


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request, pk, **kwargs):
        user = request.user
        customer = UserProfile.objects.get(pk=pk)
        if user == customer.user:
            form = UserProfileForm(instance=customer)
            return render(request, "profile.html", {"form": form})
        else:
            return HttpResponse(
                "<h1>You have entered an wrong ID to update profile</h1>"
            )

    def post(self, request, pk):
        customer = UserProfile.objects.get(pk=pk)
        form = UserProfileForm(request.POST, instance=customer)
        if form.is_valid():
            customer.first_name = form.cleaned_data.get("first_name")
            customer.nick_name = form.cleaned_data.get("nick_name")
            customer.address = form.cleaned_data.get("address")
            customer.contact = form.cleaned_data.get("contact")
            form.save()
            return redirect("/profile")
        else:
            form = UserProfileForm(instance=customer)
        return render(request, "profile.html", {"form": form})


class DeleteProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        profile = UserProfile.objects.get(pk=pk)
        if user == profile.user:
            UserProfile.objects.get(pk=pk).delete()
            return redirect("/address")
        else:
            return HttpResponse(
                "<h1>You have entered an wrong ID to delete profile</h1>"
            )
