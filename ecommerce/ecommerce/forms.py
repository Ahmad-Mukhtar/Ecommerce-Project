from django import forms

NUMS = [
    ('Customer', 'Customer'),
    ('Seller', 'Seller'),
    ('Admin', 'Admin'),
    ('Super Admin', 'Super Admin')
]


class CHOICES(forms.Form):
    NUMS = forms.CharField(widget=forms.RadioSelect(choices=NUMS,attrs={'class':'setinline'}))
