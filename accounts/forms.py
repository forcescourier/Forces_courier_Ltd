from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import Merchant, DeliverySoldier


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
    

class SoldierForm(forms.ModelForm):
    class Meta:
        model = DeliverySoldier
        exclude = ["created_at", "updated_at", "soldiers_password_hash"]  # we usually don’t edit these
        widgets = {
            "soldiers_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "soldiers_phone": forms.TextInput(attrs={"class": "form-control"}),
            "soldiers_email": forms.EmailInput(attrs={"class": "form-control"}),
            "soldiers_username": forms.TextInput(attrs={"class": "form-control"}),
            "soldiers_address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "soldiers_Blood_group": forms.TextInput(attrs={"class": "form-control"}),
            "soldiers_dob": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "soldiers_gender": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "soldiers_area_id":forms.Select(attrs={"class": "form-control"}),

            # Vehicle Info
            "soldiers_vehicle_type": forms.Select(attrs={"class": "form-control"}),
            "soldiers_vehicle_brand": forms.TextInput(attrs={"class": "form-control"}),
            "soldiers_vehicle_number": forms.TextInput(attrs={"class": "form-control"}),
            "license_expiry": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "insurance_status": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "insurance_expiry": forms.DateInput(attrs={"class": "form-control", "type": "date"}),

            # Image
            "photo": forms.FileInput(attrs={"class": "form-control-file"}),
        }
            
class SoldierAddForm(forms.ModelForm):
    soldiers_password_hash = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password"
    )

    class Meta:
        model = DeliverySoldier
        fields = [
            "photo", "soldiers_name", "soldiers_phone", "soldiers_nid",
            "soldiers_email", "soldiers_username", "soldiers_address",
            "soldiers_password_hash", "status", "soldiers_Blood_group",
            "soldiers_dob", "soldiers_gender",
            "soldiers_vehicle_type", "soldiers_vehicle_brand", "soldiers_vehicle_number",
            "license_expiry", "insurance_status", "insurance_expiry","soldiers_area_id"
        ]
        widgets = {
            "soldiers_dob": forms.DateInput(attrs={"type": "date"}),
            "license_expiry": forms.DateInput(attrs={"type": "date"}),
            "insurance_expiry": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("soldiers_password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        # hash password
        if password:
            cleaned_data["soldiers_password_hash"] = make_password(password)

        return cleaned_data