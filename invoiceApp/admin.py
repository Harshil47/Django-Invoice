

from django.contrib import admin
from .models import Orders, Customer, Product, TempRate , Record, TempTable , Billing , Payment

# Define a custom admin class for TempRate
class TempRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'location', 'product')  # Include id and other relevant fields

class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'oid', 'fname', 'Cname',
        'Lno', 'pcno', 'scno', 'product', 'df2', 'df3', 'pcs', 'amount', 'billed',
        'purchaseRate'
    )

class BillingAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'Cname', 'bill_date', 'final_amount')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('sales_challan_number', 'product', 'date', 'oid')

class RecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'Invoice', 'date', 'Cname', 'challan', 'product', 'pcs','purchaseRate')

# Register your models here
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(TempRate, TempRateAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(TempTable)
admin.site.register(Billing, BillingAdmin)
admin.site.register(Payment, PaymentAdmin)