

from django.urls import path
from . import views

urlpatterns = [
    path('parcels-info/',views.parcel, name='parcel'),
]
