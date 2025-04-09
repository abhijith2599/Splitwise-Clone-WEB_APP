from Splitz.models import *

from django import forms


class UserRegister_form(forms.ModelForm):

    class Meta:

        model = User

        fields = ['username','first_name','last_name','email','password']


        
class Login_form(forms.Form):

    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter user name'}))

    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control'}))


class Expense_form(forms.ModelForm):

    class Meta:

        model = Expense_model

        fields = ['amount','description','bill_image']


class Settle_form(forms.ModelForm):

    class Meta:

        model = SettlementModel

        fields = ['receiver','settled_amount']


class ForgotForm(forms.Form):

    username = forms.CharField(max_length=50)


class OTPform(forms.Form):

    otp = forms.IntegerField()


class PasswordChangeform(forms.Form):

    new_password = forms.CharField(max_length=50)

    confirm_password = forms.CharField(max_length=50)