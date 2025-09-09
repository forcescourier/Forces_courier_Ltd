from django.db import models

# Create your models here.

class Service(models.Model):
    service_id=models.AutoField(primary_key=True)
    service_name=models.CharField(max_length=100)
    service_price=models.DecimalField(max_digits=20, decimal_places=2)
    service_merchant_id=models.ForeignKey('accounts.Merchant',on_delete=models.CASCADE,related_name='services')
   # area many to many relation
    service_area = models.ManyToManyField('Area', related_name='service')
    def __str__(self):
        return self.service_name
  


class Area(models.Model):
    area_id=models.AutoField(primary_key=True)
    area_name=models.CharField(max_length=100)
    area_district=models.CharField(max_length=20,null=True,blank=True)
    area_station=models.CharField(max_length=50, null=True,blank=True)
    area_price=models.DecimalField(max_digits=20, decimal_places=2)
    area_category=models.CharField(max_length=50, choices=[("dhaka_city","dhaka_city"),("sub-city","sub_city"),("outside_dhaka","outside_dhaka"),], default="sub-city")
     
    
    

    def __str__(self):
        return self.area_name