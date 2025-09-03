from django.contrib import admin
from .models import Parcel, Action, Parcel_Timeline

# Register your models here.
admin.site.register(Parcel)
admin.site.register(Action)
admin.site.register(Parcel_Timeline)
