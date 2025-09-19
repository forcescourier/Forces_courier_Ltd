from django.db import models
from decimal import Decimal
from logistics.models import WeightBased
from accounts.models import SoldierEarnings
from django.db.models import F


# parcel models 


class Parcel(models.Model):
    parcels_id = models.AutoField(primary_key=True)
    parcels_merchant_id = models.ForeignKey(
        'accounts.Merchant', on_delete=models.CASCADE, null=True, blank=True, related_name='parcels'
    )
    parcels_service_id = models.ForeignKey(
        'logistics.Service', on_delete=models.CASCADE, related_name='parcels', default="1"
    )
    parcels_weight_based_id=models.ForeignKey('logistics.WeightBased', on_delete=models.CASCADE, related_name='w_parcels', null=True, blank=True)
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
    Status=[
        ('pending', 'pending'),
        ('pickup_assigned', 'pickup_assigned'),
        ('in_transit', 'in_transit'),
        ('out_of_delivery', 'out_of_delivery'),
        ('delivered', 'delivered'),
        ('returned', 'returned'),
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
    
    parcels_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g. 12.50 kg
    parcels_item_desc = models.CharField(max_length=255)
    parcels_note = models.TextField(null=True, blank=True)

    delivery_area = models.CharField(max_length=20, choices=DELIVERY_AREAS, default="dhaka")
    parcel_status= models.CharField(max_length=100, choices=Status, default="pending")
    pickup_date=models.DateField(null=True, blank=True)
    payment_method=models.CharField(max_length=200, choices=(("Bkash","Bkash"),("Nogod","Nogod"),("Bank","Bank")), null=True, blank=True, default="Bkash")

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
        weight_based=self.parcels_weight_based_id


        # Non-weight based service
        cash_collection = Decimal(self.parcels_cash_collection or 0)  # Default to 0 if None
        cod_percentage_s = Decimal(service.percentage_cod or 0)
        cod_fee = cash_collection * cod_percentage_s / Decimal(100)
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
        else:
            

        # Weight-based service
        
            weight_range = WeightBased.objects.filter(
                service=service,
                min_weight__lte=self.parcels_weight_kg,
                max_weight__gte=self.parcels_weight_kg
            ).first()

            
            if not weight_range:
                return (weight_based.base_price or 0) + cod_fee  # fallback
            
            cod_percentage_w = Decimal(weight_range.percentage_cod or 0)
            cod_fee = cash_collection * cod_percentage_w / Decimal(100)

            if self.delivery_area == 'dhaka':
                 price = weight_range.dhaka_city_price if weight_range.dhaka_city_price is not None else weight_range.base_price
                
            elif self.delivery_area == 'sub_city':
                price = weight_range.sub_city_price if weight_range.sub_city_price is not None else weight_range.base_price
                
            elif self.delivery_area == 'out_dhaka':
                price = weight_range.out_of_dhaka_price if weight_range.out_of_dhaka_price is not None else weight_range.base_price
            else: 
                price = weight_range.base_price or Decimal(0)  
               
            
            return price + cod_fee
        

    def save(self, *args, **kwargs):
        # Calculate and assign charge before saving
        self.selected_price = self.calculate_charge()

        if self.parcels_service_id and self.parcels_service_id.cod_option=="yes":
            self.parcels_service_id.customer_cod_amount = self.parcels_cash_collection
            self.parcels_service_id.save()
        
        if self.parcels_weight_based_id and self.parcels_weight_based_id.cod_option == "yes":
            self.parcels_weight_based_id.customer_cod_amount = self.parcels_cash_collection
            self.parcels_weight_based_id.save()

         # Calculate payable (Cash Collection - Charge)
        if self.parcels_cash_collection is not None and self.selected_price is not None:
            self.payable = Decimal(self.parcels_cash_collection) - Decimal(self.selected_price)
        else:
            self.payable = self.selected_price

        previous_status = None
        if self.pk:
            previous_status = Parcel.objects.filter(pk=self.pk).values_list('parcel_status', flat=True).first()

        super().save(*args, **kwargs)

        if self.parcel_status == "delivered" and previous_status != "delivered" and self.assigned_soldier:
            earnings, created = SoldierEarnings.objects.get_or_create(soldier=self.assigned_soldier)
            earnings.total_charge = F('total_charge') + (self.selected_price or 0)
            earnings.total_cod = F('total_cod') + (self.parcels_cash_collection or 0)
            earnings.total_payable = F('total_payable') + (self.payable or 0)
            earnings.save()

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
    
   