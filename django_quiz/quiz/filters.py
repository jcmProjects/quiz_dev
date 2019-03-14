import django_filters
from .models import Quiz


class QuizFilter(django_filters.FilterSet):
    paginate_by = 3;
    
    class Meta:
        model = Quiz;
        fields = {
            'course': ['icontains'],
            'question': ['icontains'],
        }