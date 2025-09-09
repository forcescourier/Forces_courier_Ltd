from django.shortcuts import render, redirect
from .forms import AreaAddForm
from . models import Service, Area
from accounts.models import DeliverySoldier
from django.db.models import Count
from django.db.models import Prefetch



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