# parcels/forms.py
from django import forms
from .models import Parcel

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = [
            "parcels_area_id",
            "parcels_service_id",
            "parcels_merchant_id",
            "parcels_customer_name",
            "parcels_customer_phone",
            "parcels_customer_phone2",
            "parcels_customer_address",
            "parcels_cash_collection",
            "parcels_type",
            "parcels_weight_kg",
            "parcels_item_desc",
            "parcels_note",
            "delivery_area",
            "pickup_date",
            "payment_method",
        ]
        widgets = {
            "parcels_customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "parcels_customer_phone": forms.TextInput(attrs={"class": "form-control"}),
            "parcels_customer_phone2": forms.TextInput(attrs={"class": "form-control"}),
            "parcels_customer_address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "parcels_cash_collection": forms.NumberInput(attrs={"class": "form-control"}),
            "parcels_type": forms.Select(attrs={"class": "form-control"}),
            "parcels_weight_kg": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "parcels_item_desc": forms.TextInput(attrs={"class": "form-control"}),
            "parcels_note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "delivery_area": forms.Select(attrs={"class": "form-control"}),
            "pickup_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "parcels_area_id": forms.Select(attrs={"class": "form-control"}),
            "parcels_service_id": forms.Select(attrs={"class": "form-control"}),
            "parcels_merchant_id":forms.Select(attrs={"class": "form-control"}),
        }
    