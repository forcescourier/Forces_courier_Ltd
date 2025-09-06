
from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='logout'),
    path('merchants/', views.merchant, name='merchant'),
    path("merchants/<str:merchant_username>/", views.view_merchant, name="view_merchant"),
    path("merchants/<str:merchant_username>/edit/", views.edit_merchant, name="edit_merchant"),
   # path("merchants/<int:merchant_id>/parcels/", views.merchant_parcels, name="merchant_parcels"),
    #path("merchants/<int:merchant_id>/payments/", views.merchant_payments, name="merchant_payments"),
]
