from django.db import models

# parcel models 


class Parcel(models.Model):
    parcels_id = models.AutoField(primary_key=True)
    parcels_merchant_id = models.ForeignKey(
        'accounts.Merchant', on_delete=models.CASCADE, related_name='parcels'
    )
    parcels_service_id = models.ForeignKey(
        'logistics.Service', on_delete=models.CASCADE, null=True, blank=True, related_name='parcels'
    )
    parcels_area_id = models.ForeignKey(
        'logistics.Area', on_delete=models.CASCADE, null=True, blank=True, related_name='parcels'
    )


    assigned_soldier = models.ForeignKey(
        'accounts.DeliverySoldier',
        on_delete=models.SET_NULL,  # If soldier is deleted, keep parcel but set null
        null=True, blank=True,
        related_name='parcels'      # 👈 this gives soldier.parcels
    )

    # Customer details
    parcels_customer_name = models.CharField(max_length=100)
    parcels_customer_phone = models.CharField(max_length=20)
    parcels_customer_phone2 = models.CharField(max_length=20, null=True, blank=True)
    parcels_customer_address = models.TextField()

    # Parcel details
    parcels_cash_collection = models.DecimalField(max_digits=10, decimal_places=2)
    parcels_weight_kg = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 12.50 kg
    parcels_item_desc = models.CharField(max_length=255)
    parcels_note = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # for tracking
    updated_at = models.DateTimeField(auto_now=True)

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
    
   