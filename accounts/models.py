from django.db import models


# Create your models here.
class Merchant(models.Model):
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

    def _str_(self):
        return self.merchant_name

# delivery soldier/rider model

class DeliverySoldier(models.Model):
    soldiers_id = models.AutoField(primary_key=True)  
    soldiers_parcel_id = models.ForeignKey('parcels.Parcel', on_delete=models.CASCADE,)
    soldiers_area_id = models.ForeignKey('logistics.Area', on_delete=models.CASCADE)
    soldiers_name = models.CharField(max_length=100)
    soldiers_phone = models.CharField(max_length=20)
    soldiers_nid = models.FileField()  # National ID
    soldiers_email = models.EmailField(unique=True)
    soldiers_username = models.CharField(max_length=50, unique=True)
    soldiers_password_hash = models.CharField(max_length=255) 
    
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