# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("payment/", views.Payment_list, name="payment"),
    path('payment-collect/',views.collect_payment, name="payment-collect"),
   
    path('soldiers/earnings/', views.soldier_earnings_view, name='soldier_earnings'),
    #path('soldiers/pay/<int:soldier_id>/', views.pay_soldier, name='pay_soldier'),
    path("pay-receive-soldier/<int:soldier_id>/", views.pay_soldier, name="pay_receive_soldier"),
]

