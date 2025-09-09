# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("area/", views.area, name="area"),
    path("add-area",views.add_area, name="add_area"),
]
