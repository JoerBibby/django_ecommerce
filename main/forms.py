from django import forms
from django.forms.widgets import CheckboxInput, RadioSelect, TextInput 


PAYMENT_OPTIONS = (
    ('S', 'Stripe'),

)

class NameForm(forms.Form):
    your_name= forms.CharField(max_length=50)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

class BillingAdressForm(forms.Form):
    address = forms.CharField(widget=TextInput(attrs={
        'placeholder': '1234 Main Street',
        
    }))
    address_2 = forms.CharField(widget=TextInput)
    country = forms.CharField(widget=TextInput)
    zip = forms.CharField(widget=TextInput)
    same_shipping_address = forms.BooleanField(widget=CheckboxInput, required=False)
    save_info = forms.BooleanField(widget=CheckboxInput, required=False)
    payment_option = forms.ChoiceField(widget=RadioSelect, choices=PAYMENT_OPTIONS)
