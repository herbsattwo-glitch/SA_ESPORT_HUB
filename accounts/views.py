from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import XboxRegistrationForm, XboxLoginForm, UserProfileUpdateForm, UserUpdateForm
from .models import UserProfile


def register_view(request):
    """
    Handles new user registration with Gamertag creation.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = XboxRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Welcome to SA Esports, {user.profile.gamertag}! Your account is ready.'
            )
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = XboxRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'page_title': 'Create Account'
    })


def login_view(request):
    """
    Handles user authentication.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = XboxLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = XboxLoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'page_title': 'Sign In'
    })


@login_required
def logout_view(request):
    """
    Logs out the current user.
    """
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been signed out.')
        return redirect('login')
    return render(request, 'accounts/logout_confirm.html')


@login_required
def profile_view(request):
    """
    Displays and updates the authenticated user's profile.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'page_title': 'My Profile'
    })


def public_profile_view(request, username):
    """
    Public view of any user's profile.
    """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'accounts/public_profile.html', {
        'viewed_user': user,
        'profile': profile,
        'page_title': f'{profile.gamertag} Profile'
    })