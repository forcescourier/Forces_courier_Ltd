

from django.urls import path
from . import views

urlpatterns = [
    path('parcels-info/',views.parcel, name='parcel'),
    path('add_parcel/', views.add_parcel, name="add_parcel"),
    path('detail/<int:parcel_id>/', views.parcel_detail, name='parcel_detail'),
    path('edit-parcel/<int:parcel_id>/', views.edit_parcel, name='edit_parcel'),
    
]
