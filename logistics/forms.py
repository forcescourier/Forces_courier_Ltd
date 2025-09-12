from django import forms
from .models import Area, Service, WeightBased

class AreaAddForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["area_name", "area_district", "area_station", "area_category", "area_price"]

        widgets = {
            "area_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter area name"}),
            "area_district": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter district"}),
            "area_station": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter station"}),
            "area_category": forms.Select(attrs={ "class": "form-control",}),
            "area_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter delivery price"}),
            
        }
class AreaEditForm(forms.ModelForm):
    class Meta:
        model= Area
        fields = ["area_name", "area_district", "area_station", "area_category", "area_price"]

        widgets = {
            "area_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter area name"}),
            "area_district": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter district"}),
            "area_station": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter station"}),
            "area_category": forms.Select(attrs={ "class": "form-control",}),
            "area_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter delivery price"}),
            
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "service_name",
            "base_price",
            "is_weight_based",
            "service_merchant_id",
            "dhaka_city_price",
            "sub_city_price",
            "out_of_dhaka_price",
            "service_parcel",
            "service_area",
            "customer_cod_amount",
            "percentage_cod",
            "calculated_cod_amount",

        ]
        widgets = {
            "service_name": forms.TextInput(attrs={"class": "form-control"}),
            "base_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "is_weight_based": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "service_area": forms.SelectMultiple(attrs={"class": "form-control"}),
            "service_merchant_id": forms.Select(attrs={"class": "form-control"}),  # ✅ fixed
            "customer_cod_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "percentage_cod": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "calculated_cod_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "readonly": True}),

        }


class WeightBasedForm(forms.ModelForm):
    class Meta:
        model = WeightBased
        fields = [
            "min_weight",
            "max_weight",
            "base_price",
            "dhaka_city_price",
            "sub_city_price",
            "out_of_dhaka_price",
            "customer_cod_amount",
            "percentage_cod",
            "calculated_cod_amount",
        ]
        widgets = {
            "min_weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "max_weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "base_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


