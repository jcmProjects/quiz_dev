from django import forms
from users.models import Course
from .models import Quiz


class ChooseCourseForm(forms.ModelForm):

    def __init__(self, auth_user, *args, **kwargs):
        super(ChooseCourseForm, self).__init__(*args, **kwargs)
        self.fields['course'] = forms.ModelChoiceField( queryset=Course.objects.filter(profile=auth_user.id) )

    class Meta:
        model = Quiz
        fields = ['course']