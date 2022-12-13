from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import unauthenticated_user
from .forms import UserUpdateForm, ProfileUpdateForm, PasswordChangeForm


@unauthenticated_user
def loginuser(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('wm-dashboard')
    context = {
        "form": form,
    }
    return render(request, 'Users/wh_login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('user-login')


def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated')
            return redirect('wm-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'Users/profile.html', context)


def landing_page_1(request):
    context = {}
    return render(request, 'Users/landing_page_1.html', context)


def slogin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('wm-dashboard')
    context = {
        "form": form,
    }
    return render(request, 'Users/supplier_login.html', context)