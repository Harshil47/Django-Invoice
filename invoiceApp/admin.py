

from django.contrib import admin
from .models import Orders, Customer, Product, TempRate , Record, TempTable , Billing

# Define a custom admin class for TempRate
class TempRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'location', 'product')  # Include id and other relevant fields

# Register your models here
admin.site.register(Orders)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(TempRate, TempRateAdmin)
admin.site.register(Record)
admin.site.register(TempTable)
admin.site.register(Billing)