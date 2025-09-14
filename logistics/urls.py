# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("area/", views.area, name="area"),
    path("add-area/",views.add_area, name="add_area"),
    path('areas/<str:area_name>/', views.view_area, name="detail_area"),
    path('areas/<str:area_name>/edit/', views.edit_area, name="edit_area"),
    path("areas/<str:area_name>/delete/", views.delete_area, name="delete_area"),
    path('service/', views.service, name='service'),
    path('add_service/',views.add_service, name='add_service'),
    path('add_weight_based/<int:service_id>/',views.add_weight_based, name="add_weight_based"),
    path("service/<int:service_id>/", views.view_service, name="view_service"),
    path("service/<int:service_id>/edit/",views.edit_service, name="edit_service"),
    path("service/<int:pk>/delete/", views.delete_service, name="delete_service"),
    
]
