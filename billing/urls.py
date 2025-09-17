# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("payment/", views.Payment_list, name="payment"),
    path('payment-collect/',views.collect_payment, name="payment-collect"),
]
