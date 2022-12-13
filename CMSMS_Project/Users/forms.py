from django import forms
from django.forms import Textarea
from .models import Profile
from django.contrib.auth.models import User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'address',
            'phone',
            'image',
        ]

        labels = {
            "bio": "About",
            "image": "Profile Picture",
        }

        widgets = {
            'bio': Textarea(attrs={'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control form-label'})
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

        labels = {
            "email": "Email",
        }


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
