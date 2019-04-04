from django import forms
from users.models import Course
from .models import Quiz
from datetime import datetime
from django.utils import timezone


class QuizForm(forms.ModelForm):

    def __init__(self, auth_user, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['course'] = forms.ModelChoiceField( queryset=Course.objects.filter(profile=auth_user.id) )  # ModelChoiceField or ModelMultipleChoiceField (the latter has a bug)

    class Meta:
        model = Quiz
        # fields = ['course']
        fields = ['course', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'right_ans', 'duration', 'image']


class QuizUploadForm(forms.ModelForm):

    def __init__(self, auth_user, *args, **kwargs):
        super(QuizUploadForm, self).__init__(*args, **kwargs)
        self.fields['author'] = forms.IntegerField(widget=forms.HiddenInput(), initial=auth_user.id)
        self.fields['date_created'] = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now())
        self.fields['start_date'] = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now())

    class Meta:
        model = Quiz
        fields = ['author', 'date_created', 'start_date']
        