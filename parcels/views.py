from django.shortcuts import render,redirect,get_object_or_404
from .models import Parcel, Action, Parcel_Timeline
from .forms import ParcelForm
from django.http import JsonResponse
from logistics.models import Service, WeightBased
from decimal import Decimal

# Create your views here.

def parcel(request):
    parcels = Parcel.objects.all().order_by('-created_at')
    #context = {"parcels": parcels}
    return render(request, "parcels/parcel.html", {'parcels': parcels})

def add_parcel(request):
    if request.method == "POST":
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            #parcel.parcels_merchant_id = request.user.merchant  # if logged-in merchant
            parcel.save()
            return redirect("parcel")  # replace with your parcel list view name
    else:
        form = ParcelForm()

    return render(request, "parcels/add_parcel.html", {"form": form} )

def parcel_detail(request, parcel_id):
    parcel = get_object_or_404(Parcel, parcels_id=parcel_id)
    # optionally, fetch related parcels by same sender or area
    related_parcels = Parcel.objects.filter(parcels_customer_phone=parcel.parcels_customer_phone).exclude(parcels_id=parcel_id)[:5]
    
    context = {
        'parcel': parcel,
        'related_parcels': related_parcels,
    }
    return render(request, 'parcels/details_parcel.html', context)

def edit_parcel(request, parcel_id):
    parcel = get_object_or_404(Parcel, pk=parcel_id)
    
    if request.method == 'POST':
        form = ParcelForm(request.POST, instance=parcel)
        if form.is_valid():
            form.save()
            return redirect('parcel_detail', parcel_id=parcel.parcels_id)  # redirect to detail page
    else:
        form = ParcelForm(instance=parcel)
    
    context = {
        'parcel': parcel,
        'form': form
    }
    return render(request, 'parcels/edit_parcel.html', context)





