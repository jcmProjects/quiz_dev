from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Course
from quiz.models import Lesson


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class ProfileQuizForm(forms.ModelForm):
    
    def __init__(self, auth_user, *args, **kwargs):
        super(ProfileQuizForm, self).__init__(*args, **kwargs)
        self.fields['course'] = forms.ModelChoiceField( queryset=Course.objects.filter(profile=auth_user.id) )  # ModelChoiceField or ModelMultipleChoiceField (the latter has a bug)

    class Meta:
        model = Lesson
        fields = ['course', 'valid_ans']