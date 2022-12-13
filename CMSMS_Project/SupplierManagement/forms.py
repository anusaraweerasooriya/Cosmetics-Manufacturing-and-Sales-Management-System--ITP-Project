from django import forms
from django.contrib.auth.models import User
from .models import Newsupplier, SupplierProduct, OrderRequest, SupplierInfo, Invoice, Order, Returns
from django.contrib.auth.forms import UserCreationForm
from WarehouseManagement.models import WarehouseRequest
from Users.models import Profile
from Users.forms import ProfileUpdateForm


class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = ['request_ID', 'itemName', 'quantity', 'due_Date', 'SupplierID', 'Note']

    def clean(self):
        cleaned_data = super(OrderRequestForm, self).clean()
        duedate = cleaned_data.get("due_Date")
        date = cleaned_data.get("date")
        if duedate and date:
            if date.now() > duedate:
                msg = "Due date should be larger than the current date"
                self.add_error('due_Date', msg)

        return self.cleaned_data

class SupplierRegisterForm(forms.ModelForm):
    class Meta:
        model = Newsupplier
        fields = ['first_name', 'last_name', 'product_category', 'address', 'contact_no', 'email', 'username', 'password']

    def clean(self):
         super(SupplierRegisterForm, self).clean()

         username = self.cleaned_data.get('username')
         password = self.cleaned_data.get('password')

         if len(username) <5:
             self._errors['username'] = self.error_class([
                 'Minimum 5 characters required'
             ])
         if len(password) <8:
             self._errors['password'] = self.error_class([
                 'Your password should contain more than 8 characters.'
             ])

         return self.cleaned_data

class CreateNewSupplierForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class SupplierInfoForm(forms.ModelForm):
    class Meta:
        model = SupplierInfo
        fields = ['address', 'contact_no', 'product_category']



class SupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        fields = ['Product', 'Unit', 'Unit_Price']
        labels = {'Product': 'PRODUCT', 'Unit': 'UNIT', 'Unit_Price': 'UNIT PRICE'}

class OrderAcceptForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['request_ID', 'price', 'invoice_image', 'invoice_pdf']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['request_ID', 'address', 'payment_image', 'further_details']
        labels = {'request_ID': '<b>Order ID</b>', 'address': '<b>Ship to</b>', 'payment_image': '<b>Attachments(payment details)</b></br><i>as image</i>', 'further_details': '<br/><b>furthur details</b>'}



class ReturnForm(forms.ModelForm):
    class Meta:
        model = Returns
        fields = ['request_ID', 'refund', 'Ship_again', 'Description']
        labels = {'request_ID': '<b>Order ID</b>', 'refund': 'Refund', 'Ship_again': 'Ship again', 'Description': '<br/><b>Description</b>'}

    def clean(self):
         super(ReturnForm, self).clean()

         refund = self.cleaned_data.get('refund')
         reship = self.cleaned_data.get('Ship_again')

         if refund == reship:
             self._errors['refund'] = self.error_class([
                 'You can select only one option'
             ])

         return self.cleaned_data


class S_ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = SupplierInfo
        fields = ['address', 'contact_no', 'product_category', 'account_no', 'bankWithBranch', 'profile_image']


class UserUpdateForm(forms.ModelForm):
    class Meta:
         model = User
         fields = ['username', 'email']


class PasswordChangeForm(forms.ModelForm):
    new_password = forms.CharField(max_length=50, min_length=8)
    reenter_password = forms.CharField(max_length=50, min_length=8)

    class Meta:
        model = User
        fields = [
            'password',
            'new_password',
            'reenter_password',
        ]