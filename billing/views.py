from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment
from django.db.models import Sum
from .forms import SoldierPaymentForm



from django.contrib import messages
from accounts.models import DeliverySoldier, SoldierEarnings
from .models import SoldierPayment

# Create your views here.

def Payment_list(request):
    payments = Payment.objects.all().order_by("-created_at")  # newest first

    # Example stats (you can refine later)
    total_collected = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
    completed = payments.filter().count()  # if you add status later
    pending = 0  # placeholder (no status in model yet)
    transactions_count = payments.count()

    context = {
        "payments": payments,
        "total_collected": total_collected,
        "completed": completed,
        "pending": pending,
        "transactions_count": transactions_count,
    }
    return render(request, 'billing/payment.html', context)


def collect_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment processed successfully ✅")
            return redirect("payment")
        else:
            messages.error(request, "There was an error with your submission ❌")
    else:
        form = PaymentForm()

    # Dummy summary – you can compute dynamically
    summary = {
        "amount": 0,
        "processing_fee": 0,
        "discount": 0,
        "total": 0,
    }

    # Grab last 5 payments
    recent_payments = Payment.objects.order_by("-created_at")[:5]

    return render(request, 'billing/payment_collect.html', {
        "form": form,
        "summary": summary,
        "recent_payments": recent_payments,
    })


def soldier_earnings_view(request):
    soldiers = DeliverySoldier.objects.all().select_related('earnings')
    context = {
        'soldiers': soldiers
    }
    return render(request, 'billing/soldier_earnings.html', context)



def pay_soldier(request, soldier_id):
    soldier = get_object_or_404(DeliverySoldier, soldiers_id=soldier_id)

    if request.method == "POST":
        form = SoldierPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.soldier = soldier
            payment.save()
            messages.success(request, f"Payment recorded for {soldier.soldiers_name}")
            return redirect("soldier_earnings")
    else:
        form = SoldierPaymentForm(initial={
            'total_charge': getattr(soldier.earnings, 'total_charge', 0),
            'total_cod': getattr(soldier.earnings, 'total_cod', 0),
            'total_payable': getattr(soldier.earnings, 'total_payable', 0),
        })

        # Reset earnings
        soldier.earnings.total_charge = 0
        soldier.earnings.total_cod = 0
        soldier.earnings.total_payable = 0
        soldier.earnings.save()    

    return render(request, "billing/pyment-receive.html", {"form": form, "soldier": soldier})