from django import forms
from .models import Area

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
