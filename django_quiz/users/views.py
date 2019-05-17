from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from quiz.models import Lesson
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm, ProfileUpdateForm, ProfileQuizForm


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

    auth_user = request.user
    print(auth_user)

    try:
        lesson = Lesson.objects.latest('id')
    except Lesson.DoesNotExist:
        lesson = None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        quiz_form = ProfileQuizForm(auth_user)

        if quiz_form.is_valid():
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')

        if u_form.is_valid() and p_form.is_valid() and quiz_form.is_valid():
            u_form.save()
            p_form.save()
            quiz_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        quiz_form = ProfileQuizForm(auth_user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'quiz_form': quiz_form,
        'lesson': lesson
    }

    return render(request, 'users/profile.html', context)


@login_required     # login is required to access profile view
def account(request):

    if request.method == 'POST':
        a_form = AccountUpdateForm(request.POST, instance=request.user)
        pass_form = PasswordChangeForm(request.user, request.POST)

        if a_form.is_valid() and pass_form.is_valid():
            a_form.save()
            user = pass_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        a_form = AccountUpdateForm(instance=request.user)
        pass_form = PasswordChangeForm(request.user)

    context = {
        'a_form': a_form,
        'pass_form': pass_form,
    }

    return render(request, 'users/account.html', context)
