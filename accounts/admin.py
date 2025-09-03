from django.contrib import admin
from .models import Merchant, DeliverySoldier, Customer

# Register your models here.
admin.site.register(Merchant)
admin.site.register(DeliverySoldier)
admin.site.register(Customer)