from django.db import models

# Create your models here.

class Service(models.Model):
    service_id=models.AutoField(primary_key=True)
    service_name=models.CharField(max_length=100)
    service_price=models.DecimalField(max_digits=20, decimal_places=2)
    service_merchant_id=models.ForeignKey('accounts.Merchant',on_delete=models.CASCADE,related_name='services')

    def __str__(self):
        return self.service_name
  


class Area(models.Model):
    area_id=models.AutoField(primary_key=True)
    area_name=models.CharField(max_length=100)
    area_post_code=models.CharField(max_length=20,unique=True,blank=True)
    area_price=models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.area_name