import os
from django.utils.text import slugify
from datetime import datetime

from django.db import models
import datetime



# Create your models here.
class Merchant(models.Model):

    STATUS_CHOICES=(
        ("pending","Pending Approval"),
        ("approved","Approved"),
        ("rejected","Rejected"),
    )
    merchant_id = models.BigAutoField(primary_key=True)
    merchant_name = models.CharField(max_length=100)
    merchant_email = models.EmailField(unique=True)
    merchant_phone = models.CharField(max_length=20)
    merchant_business_name = models.CharField(max_length=150)
    merchant_business_number = models.CharField(max_length=50)
    merchant_business_url = models.URLField(blank=True, null=True)
    merchant_pickup_address = models.TextField()
    merchant_username = models.CharField(max_length=50, unique=True)
    merchant_password = models.CharField(max_length=255)
    merchant_category = models.CharField(max_length=100)
    merchant_business_description=models.TextField(blank=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.merchant_name

# delivery soldier/rider model

def soldier_upload_path(instance, filename):
    base, ext = os.path.splitext(filename)
    safe_name = slugify(base)  # removes spaces & unsafe chars
    return f"soldier/{safe_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"


class DeliverySoldier(models.Model):

    STATUS_CHOICES=(
        ("active","active"),
        ("off_duty","off_duty"),
        ("suspended","suspended"),
    )
    soldiers_id = models.AutoField(primary_key=True)  
    soldiers_parcel_id = models.ForeignKey('parcels.Parcel', on_delete=models.CASCADE, blank=True, null=True)
    soldiers_area_id = models.ForeignKey('logistics.Area', on_delete=models.CASCADE)
    photo=models.ImageField(upload_to="soldier/", default="soldier/default.png", null=True, blank=True)
    soldiers_name = models.CharField(max_length=100)
    soldiers_phone = models.CharField(max_length=20)
    soldiers_nid = models.IntegerField(unique=True)  # National ID
    soldiers_email = models.EmailField(unique=True)
    soldiers_username = models.CharField(max_length=50, unique=True)
    soldiers_address=models.TextField()
    soldiers_password_hash = models.CharField(max_length=255) 
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    soldiers_Blood_group=models.CharField(max_length=10, null=True, blank=True)
    soldiers_dob=models.DateField(default=datetime.date.today)
    soldiers_gender=models.CharField(max_length=20,choices=(("male","male"), ("female","female"), ("others","others")))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   # vehicle info
    soldiers_vehicle_type = models.CharField(max_length=50, choices=[
        ("motorcycle", "motorcycle"),
        ("scooter", "scooter"),
        ("bicycle", "bicycle"),
        ("car", "car"),
    ], default="motorcycle")
    soldiers_vehicle_brand = models.CharField(max_length=100, blank=True, null=True)
    soldiers_vehicle_number = models.CharField(max_length=50, blank=True, null=True)  # License plate
    license_expiry = models.DateField(null=True, blank=True)
    insurance_status = models.BooleanField(default=True, blank=True, null=True)  # True = valid, False = expired
    insurance_expiry = models.DateField(null=True,blank=True )
    def __str__(self):
        return f"{self.soldiers_name} ({self.soldiers_username})"


# customer model
class Customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=100)
    customer_phone=models.CharField(max_length=20)
    customer_email=models.EmailField(unique=True)
    customer_address=models.TextField()
    customer_cod_amount=models.DecimalField(max_digits=10,decimal_places=2)
    customer_parcel_note=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.customer_name
    


    