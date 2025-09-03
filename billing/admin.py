from django.contrib import admin
from .models import Transaction, Invoice

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Invoice)
