from django import forms
from .models import Orders , Customer, Product , Billing
import math
from django.core.exceptions import ValidationError
class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'
        exclude = ['billed', 'AggregatedAmount', 'AggregatedQuantity', 'mergedOids']

        labels = {
            'fname' : 'Supplier Name',
            'Cname' : 'Customer Name',
            'Pname' : 'Place' ,
            'Dname' : 'Driver Name' ,
            'Lno' : 'Lorry number' ,
            'pcno' : 'Purchase Challan no.' ,
            'scno' : 'Sales Challan no' ,
            'product' : 'Product Name' ,
            'trip' : 'Number of trips' ,
            'df1' : 'Entry Date',
            'df2' : 'Purchase Challan Date',
            'df3' : 'Sales Challan Date',
            'pcs' : 'Quantity',
            'height' : 'height',
            'width' : 'width',
            'length' : 'length',
            
        }

        widgets  ={
            'fname' : forms.TextInput(attrs={'placeholder': 'Name of the Supplier'}),
            'Cname' : forms.TextInput(attrs={'placeholder': 'Name of the Customer'}),
            'Pname' : forms.TextInput(attrs={'placeholder': 'Location of Delivery'}),
            'Dname' : forms.TextInput(attrs={'placeholder': 'Name of the Driver'}),
            'Lno' : forms.TextInput(attrs={'placeholder': 'Name of the Driver'}),
            'pcno' : forms.TextInput(attrs={'placeholder': '?'}),
            'scno' : forms.TextInput(attrs={'placeholder': '?'}),
            'product': forms.Select(attrs={'onchange': 'updateProductDetails();'}),
            'trip' : forms.NumberInput(attrs={'placeholder': '?'}),
            'df1': forms.DateInput(attrs={'type': 'Date'}),
            'df2': forms.DateInput(attrs={'type': 'Date'}),
            'df3': forms.DateInput(attrs={'type': 'Date'}),
            'pcs' : forms.NumberInput(attrs={'placeholder': '?'}),
            'height': forms.NumberInput(attrs={'placeholder': 'Height' }),
            'width': forms.NumberInput(attrs={'placeholder': 'Width'}),
            'length': forms.NumberInput(attrs={'placeholder': 'Length'}),

            'amount': forms.HiddenInput(),
            
            
        }
        

        def clean(self):
            cleaned_data = super().clean()
            product = cleaned_data.get('product')
            quantity = cleaned_data.get('pcs')
            height = cleaned_data.get('height')
            width = cleaned_data.get('width')
            length = cleaned_data.get('length')
            if quantity is None:
                quantity = 1
                cleaned_data['pcs'] = quantity
            
            if product and product.name in ['Brick', 'SandPiece', 'Cement']:
        # Calculate amount based on quantity, rate, and quantity_per
                rate = product.rate
                quantity_per = product.quantity_per
                cleaned_data['amount'] = (rate / quantity_per) * quantity
            elif product and product.name in ['SandSqft', 'Khadi']:
        # Calculate amount based on height, width, length, rate, and quantity_per
                rate = product.rate
                quantity_per = product.quantity_per
                cleaned_data['amount'] = (height * width * length * rate) / quantity_per
                cleaned_data['pcs'] = height * width * length

        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['product'].queryset = Product.objects.all()
            
            
def calculate_amount(order_instance):
    # Add your calculation logic here based on the order_instance
    # For example:
    quantity = order_instance.pcs
    height = order_instance.height
    width = order_instance.width
    length = order_instance.length
    rate = order_instance.product.rate
    quantity_per = order_instance.product.quantity_per

    if 'Brick' in order_instance.product.name:
        # Calculate amount based on quantity, rate, and quantity_per
        amount = (rate / quantity_per) * quantity
    if 'SandPiece' in order_instance.product.name:
        # Calculate amount based on quantity, rate
        amount = rate * quantity
    if 'Cement' in order_instance.product.name:
        # Calculate amount based on quantity, rate
        amount = rate * quantity
    elif 'Khadi' in order_instance.product.name:
        # Calculate amount based on height, width, length, rate, and quantity_per
        vr_height, h = math.modf(height)
        vr_width, w = math.modf(width)
        vr_length, l = math.modf(length)
        
        vr_height = (vr_height * 100) / 12
        vr_width = (vr_width * 100) / 12
        vr_length = (vr_length * 100) / 12
        
        height = h + vr_height
        width = w + vr_width
        length = l + vr_length
        pcsQuantity = height * width * length * rate 
        amount = (pcsQuantity) / quantity_per
    elif 'SandSqft' in order_instance.product.name:
        # Calculate amount based on height, width, length, rate, and quantity_per
        vr_height, h = math.modf(height)
        vr_width, w = math.modf(width)
        vr_length, l = math.modf(length)
        
        vr_height = (vr_height * 100) / 12
        vr_width = (vr_width * 100) / 12
        vr_length = (vr_length * 100) / 12
        
        height = h + vr_height
        width = w + vr_width
        length = l + vr_length
        pcsQuantity = height * width * length * rate 
        amount = (pcsQuantity) / quantity_per
    else:
        # Add additional cases as needed
        amount = 0  # Set a default value or handle the case accordingly

    return amount
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        
        labels = {
            'Cname': 'Customer Name',
            'group' : 'Group',
            'adr' : 'Address' ,
            'phone' : 'Phone Number' ,
            'gst' : 'GST' ,
            'pan' : 'PAN' ,
        }

        widgets  ={
            'Cname' : forms.TextInput(attrs={'placeholder': 'Customer Name'}),
            'group' : forms.TextInput(attrs={'placeholder': 'Customer Group'}),
            'adr' : forms.TextInput(attrs={'placeholder': ''}),
            'phone' : forms.TextInput(attrs={'placeholder': ''}),
            'gst' : forms.TextInput(attrs={'placeholder': 'GST number'}),
            'pan' : forms.TextInput(attrs={'placeholder': 'PAN number'}),
            
            
        }
        
class BillingForm(forms.Form):
    total_rate = forms.FloatField()
    material_rate = forms.FloatField()
    bill_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        order_instance = kwargs.pop('order_instance', None)
        super(BillingForm, self).__init__(*args, **kwargs)
        self.order_instance = order_instance

    def clean(self):
        cleaned_data = super().clean()
        total_rate = cleaned_data.get('total_rate')
        material_rate = cleaned_data.get('material_rate')

        if total_rate is not None and material_rate is not None and self.order_instance is not None:
            # Perform calculations
            transport_rate = total_rate - material_rate
            amount = self.order_instance.AggregatedQuantity * total_rate

            # Add the calculated values to the cleaned data
            cleaned_data['transport_rate'] = transport_rate
            cleaned_data['amount'] = amount

        # Check if required fields are present
        required_fields = ['total_rate', 'material_rate', 'mcode', 'tcode', 'bill_date']
        for field in required_fields:
            if field not in cleaned_data:
                raise ValidationError(f'The field {field} is required.')

        return cleaned_data