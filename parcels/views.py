from django.shortcuts import render
from .models import Parcel, Action, Parcel_Timeline

# Create your views here.

def parcel(request):
    parcels = Parcel.objects.all().order_by("-created_at")
    context = {"parcels": parcels}
    return render(request, "parcels/parcel.html", context)