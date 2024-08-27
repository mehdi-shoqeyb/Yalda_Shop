from django.contrib import admin
from .models import DiscountCode,Order,OrderItem
# Register your models here.

admin.site.register(DiscountCode)
admin.site.register(Order)
admin.site.register(OrderItem)