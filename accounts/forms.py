from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import Merchant


class MerchantForm(forms.ModelForm):
    class Meta:
        model= Merchant
        fields= "__all__"


class MerchantAddForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model= Merchant
        fields=[
            "merchant_name", "merchant_email", "merchant_phone",
            "merchant_business_name", "merchant_business_number",
            "merchant_business_url", "merchant_pickup_address",
            "merchant_username", "merchant_password",
            "merchant_category", "merchant_business_description",
            "status"
        ]

        widgets={
            "merchant_password": forms.PasswordInput(),
        }
 
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("merchant_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match!")

        return cleaned_data
    
    def save(self, commit=True):
        merchant = super().save(commit=False)
        # Hash password before saving
        merchant.merchant_password = make_password(self.cleaned_data["merchant_password"])
        if commit:
            merchant.save()
        return merchant