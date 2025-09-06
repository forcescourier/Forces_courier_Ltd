
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Merchant
from .forms import MerchantForm



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

def view_merchant(request, merchant_username):
    merchant = get_object_or_404(Merchant, merchant_username=merchant_username)
    return render(request, "accounts/merchant-view.html", {"merchant": merchant})

def edit_merchant(request, merchant_username):
    merchant = get_object_or_404(Merchant, merchant_username=merchant_username)
    if request.method=="POST":
        form=MerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            print("✅ Saved:", form.cleaned_data)
            return redirect("view_merchant", merchant_username=merchant.merchant_username)
        else:
          print("❌ Errors:", form.errors)
        
    else:
        form= MerchantForm(instance=merchant)

    # For now, just render a placeholder template
    return render(request, "accounts/merchant-edit.html", {"merchant": merchant, "form": form})