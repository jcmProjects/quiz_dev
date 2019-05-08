from import_export import resources
from import_export.fields import Field
from .models import Quiz, Results


class QuizResource(resources.ModelResource):

    class Meta:
        model = Quiz
        fields = ('id', 'course', 'question', 'ansA', 'ansB', 'ansC', 'ansD', 'ansE', 'duration', 'image', 'right_ans')

