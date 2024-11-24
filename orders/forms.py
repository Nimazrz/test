from django import forms

from orders.models import Order


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=11, required=True)
    # def __init__(self, *args, **kwargs):
    #     super(PhoneForm, self).__init__(*args, **kwargs)

class CodeForm(forms.Form):
    verification_code = forms.CharField(min_length=1,max_length=6, required=True)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user_first_name', 'user_last_name', 'phone', 'email', 'city', 'province', 'address', 'postal_code',
                  'description']