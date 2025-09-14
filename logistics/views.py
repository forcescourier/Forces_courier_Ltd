from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .forms import AreaAddForm, AreaEditForm, ServiceForm, WeightBasedForm
from . models import Service, Area
from accounts.models import DeliverySoldier
from django.db.models import Count
from django.db.models import Prefetch
from django.contrib import messages



# Create your views here.
def area(request):
    areas = Area.objects.annotate(
        soldier_count=Count("deliverysoldier")
    ).prefetch_related(
        Prefetch("deliverysoldier_set", queryset=DeliverySoldier.objects.all())
    )

    context = {
        "areas": areas,
        "total_areas": areas.count(),
        "total_soldiers": DeliverySoldier.objects.filter(status="active").count(),
    }


    return render(request, "logistics/area.html", context)


def add_area(request):
    if request.method == "POST":
        form = AreaAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("area") 
    else:
        form = AreaAddForm()
    return render(request, "logistics/area-add.html", {"form": form})

def view_area(request, area_name):
    areas = (
        Area.objects.annotate(
            soldier_count=Count("deliverysoldier")
        )
        .prefetch_related(
            Prefetch("deliverysoldier_set", queryset=DeliverySoldier.objects.all())
        )  # <-- properly close Prefetch here
        .filter(area_name=area_name)
        .first()
    )

    if not areas:
        return render(request, "404.html", status=404)

    context = {
        "areas": areas,
        "total_soldiers": areas.deliverysoldier_set.filter(status="active").count(),
    }
    return render(request, "logistics/area-view.html", context)


def edit_area(request, area_name):
    areas = (
        Area.objects.annotate(
            soldier_count=Count("deliverysoldier")
        )
        .prefetch_related(
            Prefetch("deliverysoldier_set", queryset=DeliverySoldier.objects.all())
        )
        .filter(area_name=area_name)
        .first()
    )

    if not areas:
        return render(request, "404.html", status=404)

    if request.method == "POST":
        form = AreaEditForm(request.POST, instance=areas)
        if form.is_valid():
            form.save()
            return redirect("detail_area", area_name=areas.area_name)
    else:
        form = AreaEditForm(instance=areas)

    # ✅ Always available (for GET and failed POST)
    stats = {
        "total_soldiers": areas.deliverysoldier_set.filter(status="active").count(),
        "deliveries_today": 145,   # replace with real logic
        "on_time_rate": "95%",     # replace with real logic
    }
    
    return render(
        request,
        "logistics/area-edit.html",
        {"form": form, "areas": areas, "stats": stats},
    )



def delete_area(request, area_name):
    area = get_object_or_404(Area, area_name=area_name)

    if request.method == "POST":
        area.delete()
        messages.success(request, f"Area '{area.area_name}' deleted successfully.")
        return redirect("area")  # <-- redirect back to areas list page

    # For GET request, show a confirmation page
    return render(request, "logistics/area-delete.html", {"area": area})

def service(request):
    services = Service.objects.all()  # Get all services

    total_services = services.count()
    
    

    context = {
        'services': services,
        'total_services': total_services,
        
        
    }
    return render(request, 'logistics/service.html', context)

def add_service(request):
     if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            if service.is_weight_based:
                # Redirect to weight form
                return redirect("add_weight_based", service_id=service.service_id)
            else:
                return redirect("service")  # go to service list page
     else:
        form = ServiceForm()
     return render(request, 'logistics/service-add.html', {"form": form})

def add_weight_based(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == "POST":
        form = WeightBasedForm(request.POST)
        if form.is_valid():
            weight = form.save(commit=False)
            weight.service = service
            weight.save()
            return redirect("service")  # after saving weight
    else:
        form = WeightBasedForm()
    return render(request, "logistics/add_weight_based.html", {"form": form, "service": service})

def view_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, "logistics/service-view.html", {"service": service})



def edit_service(request, service_id):
    service = get_object_or_404(Service, service_id=service_id)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect("view_service", service_id=service.service_id)
    else:
        form = ServiceForm(instance=service)
    return render(request, "logistics/service-edit.html", {"form": form, "service": service})

def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect("service")  # 👈 change to your list view name
    
    return render(request, "logistics/service_delete.html", {"service": service})


