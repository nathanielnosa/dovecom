from django import forms
from . models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = ['ordered_by','shipping_address','mobile','email']
        exclude = ['order_status','subtotal','discount','amount','cart','payment_completed','ref']
        widgets={
            'order_by':forms.TextInput(attrs={'class':'form-control'}),
            'shipping_address':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
        }
