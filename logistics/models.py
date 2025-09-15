from django.db import models

# Create your models here.

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=20, decimal_places=2, null=True,blank=True)
    is_weight_based = models.BooleanField(default=False, null=True, blank=True)
    service_merchant_id = models.ForeignKey('accounts.Merchant', on_delete=models.CASCADE, related_name='services_merchant', null=True,blank=True)
    #parcel_id= models.ForeignKey('parcels.parcel', on_delete=models.CASCADE, related_name="serviceparcel", null=True,blank=True)
    customer = models.ForeignKey( "accounts.Customer", on_delete=models.CASCADE, null=True, blank=True,related_name="customerservices")
    customer_cod_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage_cod=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calculated_cod_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cod_option = models.CharField(
        max_length=10,
        choices=(("no", "No COD"), ("yes", "COD")),
        default="no"
    )
    

    dhaka_city_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    sub_city_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    out_of_dhaka_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    service_parcel = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Area many-to-many relation
    service_area = models.ManyToManyField('Area', related_name='service_area')

    def save(self, *args, **kwargs):
      
      

        if self.cod_option == "yes" and self.customer:
          #if self.parcel_id:   # ✅ check parcel exists
            #if self.customer:
              # self.customer_cod_amount = self.parcel_id.parcels_cash_collection
        
        # calculate the new COD amount based on percentage_cod
          if self.customer_cod_amount and self.percentage_cod:
            if self.dhaka_city_price:
              self.calculated_cod_amount = self.dhaka_city_price + (self.customer_cod_amount * self.percentage_cod / 100)
            elif self.sub_city_price:
              self.calculated_cod_amount = self.sub_city_price + (self.customer_cod_amount * self.percentage_cod / 100)
            elif self.out_of_dhaka_price:
              self.calculated_cod_amount = self.out_of_dhaka_price + (self.customer_cod_amount * self.percentage_cod / 100)
        
        if self.dhaka_city_price is None:
            self.dhaka_city_price = self.base_price
        if self.sub_city_price is None:
            self.sub_city_price = self.base_price
        if self.out_of_dhaka_price is None:
            self.out_of_dhaka_price = self.base_price


       
       
        super().save(*args, **kwargs)

    def __str__(self):
        return self.service_name

  
class WeightBased(models.Model):
    weight_id = models.AutoField(primary_key=True)
    #parcel_id= models.ForeignKey('parcels.parcel', on_delete=models.CASCADE, related_name="wbparcel", null=True,blank=True)
    service = models.ForeignKey("Service", on_delete=models.CASCADE, related_name='weight')
    customer = models.ForeignKey( "accounts.Customer", on_delete=models.CASCADE, null=True, blank=True,related_name="weightBasedservices")
    cod_option = models.CharField(
        max_length=10,
        choices=(("no", "No COD"), ("yes", "COD")),
        default="no"
    )
    
    customer_cod_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage_cod=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calculated_cod_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_weight = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    max_weight = models.DecimalField(max_digits=20, decimal_places=2, null=True,blank=True)
    base_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    dhaka_city_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    sub_city_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    out_of_dhaka_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # populate customer_cod_amount if customer exists
        if self.cod_option == "yes" and self.customer:
          #if self.parcel_id:   # ✅ check parcel exists
            #if self.customer:
               #self.customer_cod_amount = self.parcel_id.parcels_cash_collection
        
        # calculate the new COD amount based on percentage_cod
          if self.customer_cod_amount and self.percentage_cod:
            if self.dhaka_city_price:
               self.calculated_cod_amount = self.dhaka_city_price + (self.customer_cod_amount * self.percentage_cod / 100)
            elif self.sub_city_price:
               self.calculated_cod_amount = self.sub_city_price + (self.customer_cod_amount * self.percentage_cod / 100)
            elif self.out_of_dhaka_price:
               self.calculated_cod_amount = self.out_of_dhaka_price + (self.customer_cod_amount * self.percentage_cod / 100)

        if self.dhaka_city_price is None:
            self.dhaka_city_price = self.base_price
        if self.sub_city_price is None:
            self.sub_city_price = self.base_price
        if self.out_of_dhaka_price is None:
            self.out_of_dhaka_price = self.base_price
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Weight {self.min_weight} - {self.max_weight} for Service {self.service.service_name}"


class Area(models.Model):
    area_id=models.AutoField(primary_key=True)
    area_name=models.CharField(max_length=100)
    area_district=models.CharField(max_length=20,null=True,blank=True)
    area_station=models.CharField(max_length=50, null=True,blank=True)
    area_price=models.DecimalField(max_digits=20, decimal_places=2)
    area_category=models.CharField(max_length=50, choices=[("dhaka_city","dhaka_city"),("sub-city","sub_city"),("outside_dhaka","outside_dhaka"),], default="sub-city")
     
    
    

    def __str__(self):
        return self.area_name
    