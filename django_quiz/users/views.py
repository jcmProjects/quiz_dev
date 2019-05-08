from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required     # login is required to access profile view
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AccountUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        pass_form = PasswordChangeForm(request.user, request.POST)

        if u_form.is_valid() and p_form.is_valid() and a_form.is_valid() and pass_form.is_valid():
            u_form.save()
            a_form.save()
            p_form.save()
            user = pass_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AccountUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        pass_form = PasswordChangeForm(request.user)

    context = {
        'u_form': u_form,
        'a_form': a_form,
        'p_form': p_form,
        'pass_form': pass_form
    }

    return render(request, 'users/profile.html', context)
