from django.db import models
from decimal import Decimal


# parcel models 


class Parcel(models.Model):
    parcels_id = models.AutoField(primary_key=True)
    parcels_merchant_id = models.ForeignKey(
        'accounts.Merchant', on_delete=models.CASCADE, null=True, blank=True, related_name='parcels'
    )
    parcels_service_id = models.ForeignKey(
        'logistics.Service', on_delete=models.CASCADE, related_name='parcels', default="1"
    )
    parcels_weightbased_id=models.ForeignKey('logistics.WeightBased', on_delete=models.CASCADE, related_name='parcels', null=True, blank=True)
    parcels_area_id = models.ForeignKey(
        'logistics.Area', on_delete=models.CASCADE, null=True, blank=True, related_name='parcels'
    )


    assigned_soldier = models.ForeignKey(
        'accounts.DeliverySoldier',
        on_delete=models.SET_NULL,  # If soldier is deleted, keep parcel but set null
        null=True, blank=True,
        related_name='parcels'       # 👈 this gives soldier.parcels
    )

    DELIVERY_AREAS = [
        ('dhaka', 'Dhaka City'),
        ('sub_city', 'Sub City'),
        ('out_dhaka', 'Out of Dhaka'),
    ]

    # Customer details
    parcels_customer_name = models.CharField(max_length=100)
    parcels_customer_phone = models.CharField(max_length=20)
    parcels_customer_phone2 = models.CharField(max_length=20, null=True, blank=True)
    parcels_customer_address = models.TextField()

    # Parcel details
    parcels_cash_collection = models.DecimalField(max_digits=10, decimal_places=2)
    selected_price=models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    payable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # NEW field
    parcels_type= models.CharField(max_length=50, null=True, blank=True, choices=(("documents","documents"),("electronics","electronics"),("clothing","clothing"),("food items","food items"),("other","other")), default="other")
    parcels_weight_kg = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 12.50 kg
    parcels_item_desc = models.CharField(max_length=255)
    parcels_note = models.TextField(null=True, blank=True)

    delivery_area = models.CharField(max_length=20, choices=DELIVERY_AREAS, default="dhaka")
    pickup_date=models.DateField(null=True, blank=True)
    payment_method=models.CharField(max_length=200, choices=(("Bkash","Bkash"),("Nogod","Nogod"),("Bank","Bank")), default="Bkash")

    created_at = models.DateTimeField(auto_now_add=True)  # for tracking
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parcel {self.parcels_id} - {self.parcels_customer_name}"
    
    def calculate_charge(self):
        """
        Calculate the delivery charge based on service type (weight based or not),
        area, and parcel weight.
        """
        service = self.parcels_service_id
        weightbased=self.parcels_weightbased_id


        # Non-weight based service
        cod_fee = self.parcels_cash_collection * service.percentage_cod / 100

        if not service.is_weight_based:
           if self.delivery_area == 'dhaka':
               price = service.dhaka_city_price if service.dhaka_city_price is not None else service.base_price
           elif self.delivery_area == 'sub_city':
               price = service.sub_city_price if service.sub_city_price is not None else service.base_price
           elif self.delivery_area == 'out_dhaka':
               price = service.out_of_dhaka_price if service.out_of_dhaka_price is not None else service.base_price
           else:
              price = service.base_price or 0  # fallback

           return price + cod_fee

        # Weight-based service
        else:
            weight_range = weightbased.weight.filter(
                min_weight__lte=self.parcels_weight_kg,
                max_weight__gte=self.parcels_weight_kg
            ).first()

            
            cod_fee = self.parcels_cash_collection * weightbased.percentage_cod / 100
            if not weight_range:
                return weightbased.base_price  # fallback

            if self.delivery_area == 'dhaka':
                 price = weight_range.dhaka_city_price if weight_range.dhaka_city_price is not None else weight_range.base_price
                
            elif self.delivery_area == 'sub_city':
                price = weight_range.sub_city_price if weight_range.sub_city_price is not None else weight_range.base_price
                
            elif self.delivery_area == 'out_dhaka':
                price = weight_range.out_of_dhaka_price if weight_range.out_of_dhaka_price is not None else weight_range.base_price
            else:   
             return price + cod_fee
            
            return price + cod_fee
        

    def save(self, *args, **kwargs):
        # Calculate and assign charge before saving
        self.selected_price = self.calculate_charge()
         # Calculate payable (Cash Collection - Charge)
        if self.parcels_cash_collection is not None and self.selected_price is not None:
            self.payable =  Decimal(self.selected_price) - Decimal(self.parcels_cash_collection)
        else:
            self.payable = self.selected_price

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Parcel {self.parcels_id} - {self.parcels_customer_name}"



# action model
class Action(models.Model):
    action_id=models.AutoField(primary_key=True)
    action_parcel_id=models.ForeignKey('Parcel',on_delete=models.CASCADE,related_name='actions')
    action_name=models.CharField(max_length=100)

    def __str__(self):
        return self.action_name
    

# timeline tracking model

class Parcel_Timeline(models.Model):
    timeline_id=models.AutoField(primary_key=True)
    timeline_parcel_id=models.ForeignKey('Parcel',on_delete=models.CASCADE,related_name='timelines')
    timeline_action_id=models.ForeignKey('Action',on_delete=models.CASCADE,related_name='timelines')
    timeline_note=models.TextField(blank=True,null=True)
    timeline_created_at=models.DateTimeField(auto_now_add=True)
    timeline_updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Timeline {self.timeline_id} for Parcel {self.timeline_parcel_id.parcels_id}"
    
   