from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):

    def clean(self):
        cleaned_data2 = super().clean()
        production_price = cleaned_data2.get('production_price')
        selling_price = cleaned_data2.get('selling_price')

        if selling_price < production_price:
            error = "Selling price should be greater than the production price"
            print("Invalid price")
            self.add_error('selling_price', error)

        return cleaned_data2

    class Meta:
        model = SalesProduct
        fields = [
            'name',
            'selling_price',
            'retail_price',
            'category',
            'description',
            'production_price',
            'product_image',
            'tags',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name..'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Selling Price..'}),
            'retail_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Retail Price..'}),
            'production_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Production Price..'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Add a description..'}),
            'product_image': forms.FileInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),

        }


class UpdateProductForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        production_price = cleaned_data.get('production_price')
        selling_price = cleaned_data.get('selling_price')

        if selling_price < production_price:
            error = "Selling price should be greater than the production price"
            print("Invalid price")
            self.add_error('selling_price', error)

        return cleaned_data

    class Meta:
        model = SalesProduct
        fields = [
            'name',
            'selling_price',
            'production_price',
            'retail_price',
            'category',
            'description',
            'product_image',
            'tags',
        ]

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name..'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Selling Price..'}),
            'retail_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Retail Price..'}),
            'production_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Production Price..'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Add a description..'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name..'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name..'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name..'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email..'}),
        }


class EditProfileForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile_number', 'birth_date', 'gender',
                  'profile_picture']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name..'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name..'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name..'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email..'}),
            'mobile_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number..'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Gender..'}),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ['value', 'text_review']

        labels = {
            'value': 'Place your vote',
            'text_review': 'Add a description to your review'
        }

        widgets = {
            'value': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Place your vote'}),
            'text_review': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Add a comment with your vote'})
        }


class EditReviewForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ['value', 'text_review']

        widgets = {
            'value': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Place your vote'}),
            'text_review': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Add a comment with your vote'})
        }


class CreateSalesTeamForm(ModelForm):
    class Meta:
        model = SalesTeam
        fields = ['team_name', 'team_description', 'available', 'no_of_employees']

        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name..'}),
            'team_description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Add a description to your team'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'no_of_employees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'No of employees..'}),
        }


class UpdateSalesTeamForm(ModelForm):
    class Meta:
        model = SalesTeam
        fields = ['team_name', 'team_description', 'available']

        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name..'}),
            'team_description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Add a description to your team'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AddTeamMembersForm(ModelForm):
    class Meta:
        model = SalesTeamMembers
        fields = ['team_member']

        widgets = {
            'team_member': forms.Select(attrs={'class': 'form-select'}),
        }


class UpdateTeamMembersForm(ModelForm):
    class Meta:
        model = SalesTeamMembers
        fields = ['team_member']

        widgets = {
            'team_member': forms.Select(attrs={'class': 'form-select'}),
        }


AddSalesMembersInline = inlineformset_factory(
    SalesTeam,
    SalesTeamMembers,
    form=AddTeamMembersForm,
    extra=4,
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)


class CreateSalesTaskForm(ModelForm):
    class Meta:
        model = SalesTask
        fields = ['task_name', 'task_description', 'sales_team', 'progress', 'task_status']

        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Name..'}),
            'task_description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Task Description....'}),
            'sales_team': forms.Select(attrs={'class': 'form-control'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Progress'}),
            'task_status': forms.Select(attrs={'class': 'form-control'})
        }


class UpdateSalesTaskForm(ModelForm):
    class Meta:
        model = SalesTask
        fields = ['task_name', 'task_description', 'sales_team', 'progress', 'task_status']

        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Name..'}),
            'task_description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Task Description....'}),
            'sales_team': forms.Select(attrs={'class': 'form-control'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control'}),
            'task_status': forms.Select(attrs={'class': 'form-control'})
        }


class BulkOrderRequestForm(ModelForm):
    class Meta:
        model = BulkOrderRequest
        fields = [
            'company_name',
            'mobile_number',
            'email',
            'street_address',
            'city',
            'province',
            'zip_code',
        ]


class BulkOrderItemsForm(ModelForm):
    class Meta:
        model = BulkOrderItems
        fields = [
            'product',
            'quantity',
        ]
