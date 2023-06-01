from django import forms
from .models import Product, Category, Restaurant


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "image", "category", "restaurant"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "restaurant": forms.Select(attrs={"class": "form-control"}),
        }


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category"]
        widgets = {
            "category": forms.TextInput(attrs={"class": "form-control"}),
        }


class AddRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["title", "address", "city"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
        }
