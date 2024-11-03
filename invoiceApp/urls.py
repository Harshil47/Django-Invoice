
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.welcomeView, name='welcome_url'),
    path('od', views.orderDocView, name='orderDoc_url'),
    path('rd', views.rateDocView, name='rateDoc_url'),
    path('ofv/', views.orderFormView, name='order_url'),
    path('sv/', views.showView, name='show_url'),
    path('up/<int:f_oid>', views.updateView, name= 'update_url'),
    path('cusUp/<str:f_Cname>', views.updateCusView, name= 'update_cus_url'),
    path('del/<int:f_oid>', views.deleteView, name= 'delete_url'),
    path('cusDel/<str:f_Cname>', views.deleteCusView, name= 'delete_cus_url'),
    path('export-csv/', views.export_csv, name='export_csv_url'),
    path('customer-info/', views.customer_info, name='customer_info_url'),
    path('customer-add/', views.customer_add, name='customer_add_url'),
    path('get-product-details/<str:product_id>/', views.get_product_details, name='get_product_details'),

    path('supplier/add/', views.supplier_add, name='supplier_add_url'),
    path('supplier/update/<str:fname>/', views.updateSupplierView, name='supplier_update_url'),
    path('supplier/delete/<str:fname>/', views.deleteSupplierView, name='supplier_delete_url'),
    path('supplier/info/', views.supplier_info, name='supplier_info_url'),

    path('lorry/add/', views.lorry_add, name='lorry_add_url'),
    path('lorry/info/', views.lorry_info, name='lorry_info_url'),
    path('lorry/update/<str:Lno>/', views.updateLorryView, name='update_lorry_url'),
    path('lorry/delete/<str:Lno>/', views.deleteLorryView, name='delete_lorry_url'),
    path('get-lorry-details/<str:lorry_id>/', views.get_lorry_details, name='get_lorry_details'),

    path('product/add/', views.product_add, name='product_add_url'),
    path('product/info/', views.product_info, name='product_info_url'),
    path('product/update/<str:name>/', views.updateProductView, name='update_product_url'),
    path('product/delete/<str:name>/', views.deleteProductView, name='delete_product_url'),

    path('unpaid/<int:order_id>/', views.unpaidView, name='unpaid_url'),
    path('payments/', views.paymentView, name='payment_page_url'),
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('update_payment_date/<int:payment_id>/', views.update_payment_date, name='update_payment_date'),
    path('mark-payment-paid/<int:payment_id>/', views.mark_payment_paid, name='mark_payment_paid'),

    path('bill/', views.billView, name='bill_url'),
    path('rate/<int:id>/', views.rateView, name='rate_url'),
    path('submit/<int:id>', views.rateView, name='submit_url'),
    path('show-bill/', views.showBillView, name='showBill_url'),
    path('print-docx/', views.printDocxView, name='print_docx_url'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('analytics/total-revenue/', views.total_revenue_by_product, name='total_revenue_by_product'),
    path('analytics/average-rate/', views.average_rate_per_product, name='average_rate_per_product'),
    path('analytics/top-customers/', views.top_customer_contribution, name='top_customer_contribution'),
    path('tax-statements/', views.tax_statement_view, name='tax_statements'),

]
