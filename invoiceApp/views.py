
# Create your views here.

from django.shortcuts import redirect, render , get_object_or_404
from .forms import OrderForm,  CustomerForm , BillingForm
from .models import Orders, Customer, Product, TempRate , Billing ,  Record , TempTable , OrderGroupReference
from django.db.models import Q
import csv
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from .forms import calculate_amount
from datetime import datetime
from django.db.models import Sum, F
from django.utils.datetime_safe import datetime
from django.views.decorators.http import require_POST
from django.db.models import  Min ,Max
import itertools
from django.db import transaction
import datetime as inv_datetime 
from django.db.models import Count
from mailmerge import MailMerge
from django.template.loader import get_template
from django.http import FileResponse
import docx
from docx import Document
from docx.shared import Pt
import io, os
from num2words import num2words
from django.db.models import Value, CharField
from datetime import datetime
from django.db import transaction
import logging

def orderFormView(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_instance = form.save(commit=False)
            
            # Call the calculate_amount function and set the amount field
            order_instance.amount = calculate_amount(order_instance)
            
            # Save the order instance with the calculated amount
            order_instance.save()
            
            return redirect('show_url')
    template_name = 'invoice/order.html'
    context = {'form': form}
    return render(request, template_name, context)

def showView(request):
    supplier_query = request.GET.get('q', '')
    customer_query = request.GET.get('customer', '')
    sales_challan_date_query = request.GET.get('sales_challan_date', '')

    obj = Orders.objects.all()

    if supplier_query:
        obj = obj.filter(Q(fname__icontains=supplier_query))
    if customer_query:
        obj = obj.filter(Q(Cname__icontains=customer_query))
    if sales_challan_date_query:
        sales_challan_date = datetime.strptime(sales_challan_date_query, '%Y-%m-%d').date()
        obj = obj.filter(df3=sales_challan_date)

    template_name = 'invoice/show.html'
    context = {'obj': obj, 'query': supplier_query}
    return render(request, template_name, context)


def updateView(request, f_oid):
    obj = Orders.objects.get(oid=f_oid)
    form = OrderForm(instance=obj)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('show_url')
    template_name = 'invoice/order.html'
    context = {'form': form}
    return render(request, template_name, context)

def updateCusView(request, f_Cname):
    obj = Customer.objects.get(Cname=f_Cname)
    form = CustomerForm(instance=obj)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('customer_info_url')
    template_name = 'invoice/customer_add.html'
    context = {'form': form}
    
    return render(request, template_name, context)

def deleteView(request, f_oid):
    obj = Orders.objects.get(oid=f_oid)
    if request.method == 'POST':
        obj.delete()
        return redirect('show_url')
    template_name = 'invoice/confirmation.html'
    context = {'obj': obj}
    return render(request, template_name, context)

def deleteCusView(request, f_Cname):
    obj = Customer.objects.get(Cname=f_Cname)
    if request.method == 'POST':
        obj.delete()
        return redirect('customer_info_url')
    template_name = 'invoice/CusConfirmation.html'
    context = {'obj': obj}
    return render(request, template_name, context)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Supplier Name', 'Place', 'Driver Name', 'Lorry number', 'Purchase Challan no.', 'Sales Challan no.', 'Product Name', 'pcs/Fts', 'Number of trips', 'Date Field 1', 'Date Field 2', 'Date Field 3'])

    orders = Orders.objects.all()
    for order in orders:
        writer.writerow([order.oid, order.fname, order.Pname, order.Dname, order.Lno, order.pcno, order.scno, order.Product, order.pcs, order.trip, order.df1, order.df2, order.df3])

    return response


def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_info_url')  # Redirect to the customer info page
    else:
        form = CustomerForm()

    return render(request, 'invoice/customer_add.html', {'form': form})


def customer_info(request):
    # Get the search query from the URL parameter 'q'
    query = request.GET.get('q', '')

    # If a query is provided, filter customers based on the name
    if query:
        customers = Customer.objects.filter(Q(Cname__icontains=query))
    else:
        # If no query, fetch all customers
        customers = Customer.objects.all()

    # Render the customerInfo.html template with the customers and query
    template_name = 'invoice/customerInfo.html'
    context = {'customers': customers, 'query': query}
    return render(request, template_name, context)

def get_product_details(request, product_id):
    try:
        # Query the Product model to get details based on the product_id
        product = Product.objects.get(name=product_id)

        # Example response data
        data = {
            'name': product.name,
            'rate': product.rate,
            'quantity_per': product.quantity_per,
            # Add other fields as needed
        }

        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
 
def generate_invoice_id(model_name):
    today = inv_datetime .date.today()
    current_month = today.strftime("%b").upper()
    current_monthInt = today.month
    current_year = today.year

    # Determine financial year
    financial_year = (
        f"{current_year - 1}-{current_year % 100}"
        if current_monthInt < 4
        else f"{current_year}-{(current_year + 1) % 100}"
    )
    distinct_records = model_name.objects.filter(Invoice__endswith=f"/{financial_year}").values("Invoice").distinct()

# Display the distinct Invoice values
    print("Distinct Invoice Numbers:")
    for record in distinct_records:
        print(record["Invoice"])

    # Count the distinct records
    invoice_count = len(distinct_records)
    print("Calculated Invoice Count:", invoice_count)

    # Generate the invoice ID
    invoice_id = f"GT/{invoice_count + 1}/{current_month}/{financial_year}"

    return invoice_id


def billView(request):
    # Initialize bill_items before handling the request
    print("Request Method:", request.method)
    
    logger = logging.getLogger(__name__)
    bill_items = []
    start_date = None
    end_date = None
    #Bill Submit button       
    if request.method == "POST" and request.POST.get('action') == 'bill':
        selected_temp_rate_ids = request.POST.getlist('selected_rows')
        print("Selected Temp Rate IDs:", selected_temp_rate_ids)

        
        if selected_temp_rate_ids:
            # Fetch TempRate objects based on selected IDs
            selected_temp_rates = TempRate.objects.filter(id__in=selected_temp_rate_ids)
            print("Selected Temp Rates:", selected_temp_rates)
            
            # Merge their csoid values into a list
            merged_csoid_list = []
            for temp_rate in selected_temp_rates:
                merged_csoid_list.extend(temp_rate.csoid.split(','))

            # Process the merged OID list for billing or further actions
            print("Merged OID list:", merged_csoid_list)
            Orders.objects.filter(oid__in=merged_csoid_list).update(billed='Yes')
            
            invoice_number = generate_invoice_id(Record)
            
            for oid in merged_csoid_list:
                # Fetch data from Orders table
                order_data = Orders.objects.get(oid=oid)
                
                # Fetch data from Product table
                product_data = Product.objects.get(name=order_data.product.name)

                # Fetch data from Billing table
                billing_data = Billing.objects.get(oid=oid)
                
                customer_data = Customer.objects.get(Cname=order_data.Cname)
                
                temp_table = TempTable.objects.get(pk=1)
                end_date_from_temp_table = temp_table.end_date
                # Additional data for the Record table
                Cname = order_data.Cname
                Cadr = customer_data.adr
                Sadr = order_data.Pname
                state = customer_data.state
                code = customer_data.code
                gst = customer_data.gst
                date = order_data.df3  
                lorry_no = order_data.Lno
                trip = order_data.trip
                challan = order_data.scno
                hsn = product_data.hsn_code
                tax_rate = product_data.tax_rate
                product = order_data.product.name
                pcs = order_data.pcs
                rate = billing_data.final_rate
                amount = order_data.amount
                cgst = amount * (product_data.tax_rate / 200)
                sgst = amount * (product_data.tax_rate / 200)
                final_amount = amount + cgst + sgst
                
                print(final_amount)
                # Create a Record object and save it to the database
                record = Record.objects.create(
                    Cname = Cname,
                    Cadr = Cadr,
                    Sadr = Sadr,
                    state = state,
                    code = code,
                    gst = gst,
                    date=date,
                    InvoiceEnd=end_date_from_temp_table,
                    Invoice = invoice_number,
                    lorry_no=lorry_no,
                    trip=trip,
                    challan=challan,
                    hsn=hsn,
                    tax_rate = tax_rate,
                    product=product,
                    pcs=pcs,
                    rate=rate,
                    amount=amount,
                    cgst=cgst,
                    sgst=sgst,
                    final_amount=final_amount,
                )
            filtered_records = Record.objects.filter(Invoice=invoice_number)

# Calculate the sum of the final amount for the filtered records
            total_amount_sum = filtered_records.aggregate(Sum('final_amount'))['final_amount__sum']

# Update the 'total_amount' column for the filtered records
            filtered_records.update(total_amount=total_amount_sum)

            return redirect('showBill_url') 
    #if request.method == 'POST':
        # Clear the TempRate table on every POST request
    TempRate.objects.all().delete()
    selected_customer = request.GET.get('customer', '')
    

    # Handle the case where a date range is selected
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Parse dates if provided
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        start_date = None

    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        end_date = None
        
    temp_table, created = TempTable.objects.get_or_create(pk=1)
    temp_table.end_date = end_date
    temp_table.save()
    if start_date and end_date:
        # Filter orders within the date range
        orders = Orders.objects.filter(df3__range=(start_date, end_date), billed='No')
    if selected_customer:
        # Filter by customer name (adjust field name to match your Orders model)
        orders = orders.filter(Cname=selected_customer)
    else:
        # Fetch all unbilled orders if no date range is provided
        orders = Orders.objects.filter(billed='No')

    # Group and aggregate by customer, location, and product
   
    
    for key, group in itertools.groupby(orders.values('Cname', 'Pname', 'product', 'trip', 'pcs', 'amount', 'oid'),
                                        key=lambda x: (x['Cname'], x['Pname'], x['product'])):
        group_list = list(group)
        if group_list:
            merged_oids = ','.join(str(item['oid']) for item in group_list)
            total_trips = sum(item['trip'] for item in group_list)
            total_quantity = sum(item['pcs'] for item in group_list)
            total_amount = sum(item['amount'] for item in group_list)

            # Insert aggregated data into TempRate
            temp_rate = TempRate.objects.create(
                customer_name=key[0],  # Use the actual model field names here
                location=key[1],
                product=key[2],
                csoid=merged_oids
            )

            # Now include the TempRate id in the bill_item for linking purposes
            bill_items.append({
                'Cname': key[0],
                'Pname': key[1],
                'product': key[2],
                'csoid': merged_oids,
                'total_trips': total_trips,
                'total_pcs': total_quantity,
                'total_amount': total_amount,
                'temp_rate_id': temp_rate.id  # Include the TempRate ID
            })
            
 

    # Redirect or render the page after processing
    logger.debug("Bill Items: %s", bill_items)
    print(bill_items)
        #return redirect('show_url')

    # Handle GET requests and populate the form
    template_name = 'invoice/Bill.html'
    selected_customer = request.GET.get('customer', '')  # Moved this line here

    context = {
        'customer_names': Customer.objects.values_list('Cname', flat=True).distinct(),
        'bill_items': bill_items,  # The aggregated bill items you want to display
        'selected_customer': selected_customer,  # Customer selected by the user
        'start_date': start_date,  # Start date for filtering
        'end_date': end_date,  # End date for filtering
    }

    return render(request, template_name, context)




def rateView(request, id):
    # Fetch the TempRate object using the passed 'id' (which is the TempRate id)
    try:
        temp_rate = TempRate.objects.get(id=id)
    except TempRate.DoesNotExist:
        # Handle the case where TempRate does not exist
        return redirect('error_url')  # Redirect to an error page or handle gracefully

    # Get the comma-separated OIDs from the TempRate object
    csoid = temp_rate.csoid
    oid_list = csoid.split(',')  # Split the csoid into a list of OIDs

    # Fetch the orders corresponding to the OIDs in csoid
    orders = Orders.objects.filter(oid__in=oid_list)
    aggregated_quantity = orders.aggregate(Sum('pcs'))['pcs__sum']
    aggregated_amount = orders.aggregate(Sum('amount'))['amount__sum']
    
    if orders.exists():
        first_order = orders.first()
        customer_name = first_order.Cname
        bill_date = first_order.df1

    if request.method == "POST":
        print("POST request received")
        total_rate = float(request.POST.get('total_rate'))  # Get the total rate from the form
        oid = request.POST.get('oid')
        product = request.POST.get('product')
        place = request.POST.get('place')
        material_rate = request.POST.get('material_rate')
        transport_rate = total_rate - float(material_rate)
        # Update all orders with the new rate * quantity
        for order in orders:
            amount = order.pcs * total_rate
            order.amount = amount  # Update the aggregated amount
            order.save()  # Save changes to the database

        # Display customer name and date of the first order
        if orders.exists():
            first_order = orders.first()
            customer_name = first_order.Cname  # Assuming Cname is the customer name field
            bill_date = first_order.df1  # Assuming df1 is the bill date field

        if 'action' in request.POST and request.POST['action'] == 'submit':
            

            for order in orders:
                existing_billing = Billing.objects.filter(oid=order.oid)
        
                if existing_billing.exists():
            # Delete the existing billing records
                    existing_billing.delete()
                    
                billing_instance = Billing(
                Cname=customer_name,
                bill_date= bill_date,
                final_rate=total_rate,
                material_rate=material_rate,
                transport_rate=transport_rate,
                final_amount=order.amount,
                oid=order.oid,
                product=order.product,
                place= order.Pname
                )

            #print("Billing Data:", billing_instance.product)
                billing_instance.save()
            #print("Billing Data:", billing_instance.oid)
        
        # Fetch previous bills based on customer name and product
        

        # Pass the necessary context data to the template
        context = {
            'customer_name': customer_name,
            'bill_date': bill_date,
            'orders': orders,
            
        }
        
        return render(request, 'invoice/bill.html', context)
    previous_bills = Billing.objects.filter(
            Cname=first_order.Cname, 
            product=first_order.product
        ).order_by('-bill_date')
    # If the request method is not POST, just display the rate page with current data
    context = {
        'orders': orders,
        'customer_name': temp_rate.customer_name,  # You can use fields from TempRate here
        'location': temp_rate.location,
        'product': temp_rate.product,
        'aggregated_quantity': aggregated_quantity,
        'aggregated_amount': aggregated_amount,
        'temp_rate': temp_rate,
        'previous_bills': previous_bills,
    }
    print("Previous Bill",previous_bills)
    print(orders)
    return render(request, 'invoice/rate.html', context)

def showBillView(request):
    customer_query = request.GET.get('customer', '')
    date_query = request.GET.get('date', '')

    # Retrieve distinct records based on the 'Invoice' field
    records = Record.objects.values('Invoice').annotate(
        record_id=Max('record_id'),
        date=Max('date'),
        customer=Max('Cname'),
        total_amount=Max('total_amount'),
    ).order_by('-date')

    if customer_query:
        records = records.filter(Q(customer__icontains=customer_query))
    if date_query:
        date = datetime.strptime(date_query, '%Y-%m-%d').date()
        records = records.filter(date=date)

    template_name = 'invoice/showBill.html'
    context = {'records': records}
    return render(request, template_name, context)



def replace_placeholders(template_path, output_path, replacements):
    template = MailMerge(template_path)
    template.merge(**replacements)
    template.write(output_path)
    
def add_rows_to_table(doc, query_set):
    # Access the predefined table (assuming it's the first table in the document)
    table = doc.tables[0]

    # Iterate through the queryset and add rows to the table
    for index, record in enumerate(query_set):
        # Add a new row to the table
        row_cells = table.add_row().cells

        # Populate the cells with data from the queryset
        row_cells[0].text = record.date.strftime("%b %d") #str(record.date)
        row_cells[1].text = record.lorry_no
        row_cells[2].text = str(record.trip)
        row_cells[3].text = record.challan
        row_cells[4].text = record.hsn
        row_cells[5].text = record.product
        row_cells[6].text = str(record.pcs)
        row_cells[7].text = str(record.rate)
        row_cells[8].text = str(record.amount)
        row_cells[9].text = f"{round(record.cgst, 2)} ({str(record.tax_rate / 2)})"
        row_cells[10].text = f"{round(record.sgst, 2)} ({str(record.tax_rate / 2)})"
        row_cells[11].text = str(record.final_amount)

        
        if index == len(query_set) - 1:
           
            total_amount_row = table.add_row().cells
            total_amount_cell = total_amount_row[6].merge(total_amount_row[8])
            total_amount_cell.text = f'Total Amount : {round(record.total_amount)}'


            
            # Add a new row for 'Rupees' and the total amount in words
            rupees_row = table.add_row().cells
            rupees_cell = rupees_row[0].merge(rupees_row[1])
            rupees_cell.text = 'Rupees'

            # Add the total amount in words
            words = num2words(round(record.total_amount), lang='en_IN')
            capitalized_words = words.title()
            #amount_in_words_row = table.add_row().cells
            amount_in_words_cell = rupees_row[2].merge(rupees_row[11])
            amount_in_words_cell.text = capitalized_words

def printDocxView(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice_id')

        # Load the DOCX template file
        template_path = 'invoiceApp/templates/invoice/InVoice.docx'
        output_path = f'modified_invoice_{invoice_id.replace("/", "_")}.docx'

        # Get records based on the invoice_id
        record = Record.objects.filter(Invoice=invoice_id).first()

        # Convert all fields to strings
        Cname = str(record.Cname)
        state = str(record.state)
        code = str(record.code)
        Cadr = str(record.Cadr)
        Sadr = str(record.Sadr)
        gst = str(record.gst)
        date = str(record.InvoiceEnd)  

        # Define replacements for placeholders
        replacements = {
            'Cname': Cname,
            'invoice_id': invoice_id,
            'Cadr': Cadr,
            'state': state,
            'code': code,
            'gst': gst,
            'Sadr': Sadr,
            'date': date, 

        }
        replace_placeholders(template_path, output_path, replacements)
        
        doc = Document(output_path)

        # Your queryset
        query_set = Record.objects.filter(Invoice=invoice_id)

        # Add rows to the table
        add_rows_to_table(doc, query_set )

        # Save the modified DOCX document
        doc.save(output_path)

        # Save the modified DOCX document to a BytesIO buffer
        buffer = io.BytesIO()
        with open(output_path, 'rb') as file:
            buffer.write(file.read())

        # Create a FileResponse and return it for download
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=modified_invoice_{invoice_id.replace("/", "_")}.docx'
        response.write(buffer.getvalue())
        return response
        