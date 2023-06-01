from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["full_name", "nick_name", "address", "contact"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "nick_name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "contact": forms.TextInput(attrs={"class": "form-control"}),
        }
