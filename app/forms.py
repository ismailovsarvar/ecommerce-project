from django import forms

from app.models import Product


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.FloatField()
    rating = forms.FloatField()
    discount = forms.IntegerField()
    quantity = forms.IntegerField()


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = ['name', 'description', 'price', 'rating', 'discount', 'quantity']
        exclude = ()


# SENDING EMAIL FORMS

class EmailForm(forms.Form):
    from_email = forms.EmailField(label='From Email')
    to_email = forms.EmailField(label='To Email')
    subject = forms.CharField(max_length=100, label='Subject')
    message = forms.CharField(widget=forms.Textarea, label='Message')

