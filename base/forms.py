from django.contrib.auth.models import User
from django import forms
from .models import Shipping

class SignUpForm(forms.ModelForm) :
    password = forms.CharField(widget=forms.PasswordInput , label='password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password']
        
    def clean(self):
        cleaned_data =  super().clean()
        password= cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password :
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['full_name', 'email', 'address', 'phone']

    # تحسين شكل الـ Address
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your full address...'
        })
    )

    # باقي الحقول
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
