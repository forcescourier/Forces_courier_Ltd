
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Merchant, DeliverySoldier
from logistics.models import Area
from .forms import MerchantForm, MerchantAddForm, SoldierForm, SoldierAddForm
import io
import pandas as pd
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from django.db.models import Count
from parcels.models import Parcel




# Super-user login|Logout views
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a superuser.')

    return render(request, 'accounts/admin_login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin-login')  # after complete dashboard, use (core/dashboard.html)


# merchant function

def merchant(request):
    merchants= Merchant.objects.all().order_by("-created_at")
    total_merchants=Merchant.objects.count()
    active_merchants=Merchant.objects.filter(status="approved").count()
    pending_merchants=Merchant.objects.filter(status="pending").count()
    suspend_merchants=Merchant.objects.filter(status="rejected").count()



    context={
        "merchants":merchants,
        "total_merchants":total_merchants,
        "active_merchants":active_merchants,
        "pending_merchants":pending_merchants,
        "suspend_merchants":suspend_merchants,
             
          }
    return render(request, 'accounts/merchant.html', context)

# function for views the merchant details

def view_merchant(request, merchant_username):
    merchant = get_object_or_404(Merchant, merchant_username=merchant_username)
    return render(request, "accounts/merchant-view.html", {"merchant": merchant})

# function for editing merchant

def edit_merchant(request, merchant_username):
    merchant = get_object_or_404(Merchant, merchant_username=merchant_username)
    if request.method=="POST":
        form=MerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect("view_merchant", merchant_username=merchant.merchant_username)
        
    else:
        form= MerchantForm(instance=merchant)

    return render(request, "accounts/merchant-edit.html", {"merchant": merchant, "form": form})
# ADD merchant func
def add_merchant(request):
    if request.method == "POST":
        form = MerchantAddForm(request.POST)
        if form.is_valid():
            form.save()
            print("save")
            return redirect("merchant") 
    else:
        form = MerchantAddForm() 
        print("wrong") 
    return render(request, "accounts/merchant-add.html", {"form": form})

# merchant information export page
def export_page(request):
    return render(request, "accounts/export.html") 

#merchant info export 
def export_merchants(request):
    merchants = Merchant.objects.all()

    # --- Filters ---
    status = request.GET.get("status")
    if status and status != "all":
        merchants = merchants.filter(status=status)

    date_range = request.GET.get("date_range")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if date_range == "custom" and start_date and end_date:
        merchants = merchants.filter(created_at__date__range=[start_date, end_date])
    elif date_range == "today":
        merchants = merchants.filter(created_at__date=timezone.now().date())
    elif date_range == "yesterday":
        merchants = merchants.filter(created_at__date=timezone.now().date() - timedelta(days=1))
    elif date_range == "last7days":
        merchants = merchants.filter(created_at__date__gte=timezone.now().date() - timedelta(days=7))
    elif date_range == "last30days":
        merchants = merchants.filter(created_at__date__gte=timezone.now().date() - timedelta(days=30))

    # --- Field selection from checkboxes ---
    default_fields = [
        "merchant_id",
        "merchant_business_name",
        "merchant_name",
        "merchant_phone",
        "merchant_email",
        "status",
        "created_at",
    ]
    selected_fields = request.GET.getlist("fields")
    if not selected_fields:
        selected_fields = default_fields  # fallback if none selected

    merchants = merchants.values(*selected_fields)

    # --- Convert queryset → DataFrame AFTER filtering ---
    df = pd.DataFrame(list(merchants))

    # Fix timezone issue for Excel
    for col in df.select_dtypes(include=["datetimetz"]).columns:
        df[col] = df[col].dt.tz_localize(None)

    export_format = request.GET.get("format", "xlsx")

    # --- Exports ---
    if export_format == "xlsx":
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="merchants_export.xlsx"'
        df.to_excel(response, index=False)
        return response

    elif export_format == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="merchants.csv"'
        df.to_csv(path_or_buf=response, index=False)
        return response

    elif export_format == "json":
        response = HttpResponse(content_type="application/json")
        response["Content-Disposition"] = 'attachment; filename="merchants.json"'
        response.write(df.to_json(orient="records", indent=4))
        return response

    elif export_format == "pdf":
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Merchants Report", styles["Heading1"]))

        # Convert DataFrame to table
        if not df.empty:
            data = [df.columns.tolist()] + df.values.tolist()
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph("No data available", styles["Normal"]))

        doc.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="merchants.pdf"'
        return response

    return HttpResponse("Invalid export format", status=400)


# rider func
def soldier(request):
    
    soldiers = (
        DeliverySoldier.objects
        .select_related("soldiers_area_id")      
        .prefetch_related("parcels")            
    )

    # Statistics
    total_soldiers = soldiers.count()
    active_soldiers = soldiers.filter(status="active").count()
    off_duty = soldiers.filter(status="off_duty").count()
    suspended = soldiers.filter(status="suspended").count()

    # total parcels from FK relation (if each soldier has one parcel_id only)
    total_parcels = soldiers.aggregate(total=Count("soldiers_parcel_id"))["total"] or 0

    context = {
        "soldiers": soldiers,
        "total_soldiers": total_soldiers,
        "active_soldiers": active_soldiers,
        "off_duty": off_duty,
        "suspended": suspended,
        "total_parcels": total_parcels,
    }
    return render(request, "accounts/soldier.html", context)


def soldier_detail(request, soldiers_name):
    # Get soldier by ID with related area + parcels
    soldier = get_object_or_404(
        DeliverySoldier.objects.select_related("soldiers_area_id").prefetch_related("parcels"),
        soldiers_name=soldiers_name
    )

    # Statistics
    total_deliveries = soldier.parcels.count()
    recent_deliveries = soldier.parcels.order_by("-created_at")[:5]  # last 5
    monthly_earnings = 1245  # for now, hardcoded; later calculate
    rating = 4.8  # placeholder

    context = {
        "soldier": soldier,
        "total_deliveries": total_deliveries,
        "recent_deliveries": recent_deliveries,
        "monthly_earnings": monthly_earnings,
        "rating": rating,
    }
    return render(request, "accounts/soldier-view.html", context)

def soldier_edit(request, soldiers_name):
    soldier = get_object_or_404(DeliverySoldier, soldiers_name=soldiers_name)

    if request.method == "POST":
        form = SoldierForm(request.POST, request.FILES, instance=soldier)
        if form.is_valid():
            form.save()
            return redirect("soldier_detail" , soldiers_name=soldier.soldiers_name)
    else:
        form = SoldierForm(instance=soldier)

    return render(request, "accounts/soldier-edit.html", {"form": form, "soldier": soldier})

# add soldier func
def soldier_add(request):
     areas = Area.objects.all()
     if request.method == "POST":
        form = SoldierAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("soldier")  # create this url for soldier list page
     else:
        form = SoldierAddForm()
     return render(request, "accounts/soldier-add.html", {"form": form, "areas":areas})


def delete_soldier(request, soldiers_name):
    soldier = get_object_or_404(DeliverySoldier, soldiers_name=soldiers_name)
    if request.method == "POST":
        soldier.delete()
        return redirect("soldier")  # update to your soldier list view name
    return render(request, "accounts/soldier-delete.html", {"soldier": soldier})

